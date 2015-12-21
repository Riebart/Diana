#ifndef BSON_HPP
#define BSON_HPP

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

// Partial implementation of bson that is self-contained and simple, both implementation
// and API.
//
// Because of how it is architected, it is intended for smaller messages as it does not
// support streaming input mechanisms.
//
// It supports reading flat documents (documents without nested documents), and types:
//     1, 2, 3, 4, 5 (subtype 0), 9, 16, 17, 18
//
// It supports reading flat documents (documents without nested documents), and types:
//     (in their hex ID) 1, 2, 8, 9, 10, 11, 12
//
// See: http://bsonspec.org/spec.html and http://bsonspec.org/faq.html

class BSONReader
{
public:
    // Every element is returned in this structure, with the type field and the relevant
    // value member filled. Other values that don't map to the type are not guaranteed to
    // have any reasonable values.
    struct Element
    {
        int8_t type;
        int8_t subtype;
        char* name;

        bool     bln_val;
        int32_t  i32_val;
        int64_t  i64_val;
        double   dbl_val;

        int32_t  bin_len;
        uint8_t* bin_val;

        char*    str_val;
        int32_t  str_len;
    };

    enum ElementTypes
    {
        EndOfDocument, Double, String, SubDocument, Array, Binary, Deprecatedx06, ObjectId,
        Boolean, UTCDateTime, Null, Regex, DBPointer, JavaScript, Deprecatedx0E,
        JavaScriptWScope, Int32, MongoTimeStamp, Int64, MinKey = (int8_t)0xFF, MaxKey = 0x7F
    };

    BSONReader(char* _msg)
    {
        this->msg = _msg;
        len = *(int32_t*)(msg);
        pos = 4;
    }

    struct Element get_next_element()
    {
        // Return a sentinel -1 type when we reach the end of the message
        if ((int32_t)pos >= len)
        {
            el.type = -1;
            return el;
        }

        el.type = *(int8_t*)(msg + pos);
        pos += 1;

        // If it's an EOF document, it doesn't have a name, so don't try that. Just return.
        if (el.type == ElementTypes::EndOfDocument)
        {
            return el;
        }
        else
        {
            // Otherwise, read the name.
            el.name = msg + pos;
            pos += cstring_end();
        }

        // Switch on the element types.
        switch (el.type)
        {
        case ElementTypes::Double:
            el.dbl_val = *(double*)(msg + pos);
            pos += 8;
            break;

        case ElementTypes::String:
        case ElementTypes::JavaScript:
        case ElementTypes::Deprecatedx0E:
            el.str_len = *(int32_t*)(msg + pos);
            pos += 4;
            el.str_val = msg + pos;
            pos += el.str_len;
            break;

        case ElementTypes::SubDocument:
        case ElementTypes::Array:
            // Just eat the 'length' field for the subdocument, we don't care.
            pos += 4;
            break;

        case ElementTypes::Binary:
            el.bin_len = *(int32_t*)(msg + pos);
            pos += 4;
            el.subtype = *(int8_t*)(msg + pos);
            pos += 1;
            el.bin_val = (uint8_t*)(msg + pos);
            pos += el.bin_len;
            break;

        case ElementTypes::Deprecatedx06:
        case ElementTypes::Null:
        case ElementTypes::MinKey:
        case ElementTypes::MaxKey:
            break;

        case ElementTypes::ObjectId:
            el.bin_len = 12;
            el.bin_val = (uint8_t*)(msg + pos);
            pos += 12;

        case ElementTypes::Boolean:
            el.bln_val = *(bool*)(msg + pos);
            pos += 1;
            break;

        case ElementTypes::Regex:
            pos += cstring_end();
            pos += cstring_end();
            break;

        case ElementTypes::UTCDateTime:
        case ElementTypes::MongoTimeStamp:
        case ElementTypes::Int64:
            el.i64_val = *(int64_t*)(msg + pos);
            pos += 8;
            break;

        case ElementTypes::Int32:
            el.i32_val = *(int32_t*)(msg + pos);
            pos += 4;
            break;
        }

        return el;
    }

private:
    struct Element el;
    int32_t len;
    uint64_t pos;
    char* msg;

    BSONReader()
    {
    }

    int32_t cstring_end()
    {
        int i = 0;
        for (; msg[pos + i] != 0; i++) {}
        return i + 1;
    }
};

class BSONWriter
{
public:
    BSONWriter()
    {
        // Allocate enough memory for the length starting field.
        // Each time we push something, we will realloc the block a bit bigger.
        out = (uint8_t*)calloc(1, 4);
        if (out == NULL)
        {
            throw "OOM you twat";
        }

        is_array = -1;
        pos = 4;
        child = NULL;
        parent = NULL;
    }

    bool push_int32(char* name, int32_t v)
    {
        if (child != NULL)
        {
            return child->push_int32(name, v);
        }
        else
        {
            name = (is_array != -1 ? print_array_name() : name);
            int32_t name_len = (int32_t)(strlen(name) + 1);
            enlarge(1 + name_len + 4);
            out[pos] = BSONReader::ElementTypes::Int32;
            pos += 1;
            memcpy(out + pos, name, name_len);
            pos += name_len;
            *(int32_t*)(out + pos) = v;
            pos += 4;
            return true;
        }
    }

    bool push_int64(char* name, int64_t v, int8_t type = BSONReader::ElementTypes::Int64)
    {
        if (child != NULL)
        {
            return child->push_int64(name, v, type);
        }
        else
        {
            name = (is_array != -1 ? print_array_name() : name);
            int32_t name_len = (int32_t)(strlen(name) + 1);

            switch (type)
            {
            case BSONReader::ElementTypes::Int64:
            case BSONReader::ElementTypes::UTCDateTime:
            case BSONReader::ElementTypes::MongoTimeStamp:
                enlarge(1 + name_len + 8);
                out[pos] = type;
                pos += 1;
                memcpy(out + pos, name, name_len);
                pos += name_len;
                *(int64_t*)(out + pos) = v;
                pos += 8;
                return true;
            default:
                return false;
            }
        }
    }

    bool push_double(char* name, double v)
    {
        if (child != NULL)
        {
            return child->push_double(name, v);
        }
        else
        {
            name = (is_array != -1 ? print_array_name() : name);
            int32_t name_len = (int32_t)(strlen(name) + 1);
            enlarge(1 + name_len + 8);
            out[pos] = BSONReader::ElementTypes::Double;
            pos += 1;
            memcpy(out + pos, name, name_len);
            pos += name_len;
            *(double*)(out + pos) = v;
            pos += 8;
            return true;
        }
    }

    bool push_string(char* name, char* v, size_t len = -1, int8_t type = BSONReader::ElementTypes::String)
    {
        if (child != NULL)
        {
            return child->push_string(name, v, len, type);
        }
        else
        {
            if (len < 0)
            {
                len = strlen(v);
            }
            name = (is_array != -1 ? print_array_name() : name);
            int32_t name_len = (int32_t)(strlen(name) + 1);

            switch (type)
            {
            case BSONReader::ElementTypes::String:
            case BSONReader::ElementTypes::JavaScript:
            case BSONReader::ElementTypes::Deprecatedx0E:
                enlarge(1 + name_len + 4 + len + 1); // Type, name, str_len, string, 0x00
                out[pos] = type;
                pos += 1;
                memcpy(out + pos, name, name_len);
                pos += name_len;
                *(int32_t*)(out + pos) = (int32_t)(len + 1); // string + 0x00
                pos += 4;
                memcpy(out + pos, v, len);
                pos += len;
                out[pos] = 0;
                pos += 1;
                return true;
            default:
                return false;
            }
        }
    }

    bool push_binary(char* name, uint8_t* bin, int32_t len, uint8_t subtype = 0)
    {
        if (child != NULL)
        {
            return child->push_binary(name, bin, len, subtype);
        }
        else
        {
            name = (is_array != -1 ? print_array_name() : name);
            int32_t name_len = (int32_t)(strlen(name) + 1);
            enlarge(1 + name_len + 1 + len); // Type, name, subtype, length
            out[pos] = BSONReader::ElementTypes::Binary;
            pos += 1;
            memcpy(out + pos, name, name_len);
            pos += name_len;
            *(uint8_t*)(out + pos) = subtype;
            pos += 1;
            memcpy(out + pos, bin, len);
            pos += len;
            return true;
        }
    }

    int32_t push_array(char* name)
    {
        if (child != NULL)
        {
            return child->push_array(name);
        }
        else
        {
            name = (is_array != -1 ? print_array_name() : name);
            int32_t name_len = (int32_t)(strlen(name) + 1);
            enlarge(1 + name_len);
            out[pos] = BSONReader::ElementTypes::Array;
            pos += 1;
            memcpy(out + pos, name, name_len);
            pos += name_len;

            child = new BSONWriter(this, 0);
            return 0;
        }
    }

    int32_t push_subdoc(char* name)
    {
        if (child != NULL)
        {
            return child->push_subdoc(name);
        }
        else
        {
            name = (is_array != -1 ? print_array_name() : name);
            int32_t name_len = (int32_t)(strlen(name) + 1);
            enlarge(1 + name_len);
            out[pos] = BSONReader::ElementTypes::SubDocument;
            pos += 1;
            memcpy(out + pos, name, name_len);
            pos += name_len;

            child = new BSONWriter(this);
            return 0;
        }
    }

    uint8_t* push_end()
    {
        if (child != NULL)
        {
            uint8_t* child_out = child->push_end();
            if (child_out != NULL)
            {
                int32_t child_len = *(int32_t*)child_out;
                enlarge(child_len);
                memcpy(out + pos, child_out, child_len);
                pos += child_len;
                //free(child_out); // Note that this happens during the child's destructor.
                delete child;
                child = NULL;
            }
            return NULL;
        }
        else
        {
            enlarge(1);
            out[pos] = 0;
            *(int32_t*)out = (int32_t)(pos + 1); // Set the first 4 bytes to the length
            return out;
        }
    }

    ~BSONWriter()
    {
        free(out);
    }
protected:
    BSONWriter(BSONWriter* _parent, int32_t _is_array = -1)
    {
        out = (uint8_t*)calloc(1, 4);
        if (out == NULL)
        {
            throw "OOM you twat";
        }

        is_array = _is_array;
        pos = 4;
        child = NULL;
        parent = _parent;
    }

private:
    uint8_t* out;
    int32_t is_array = -1;
    char array_name[10];
    uint64_t pos;
    BSONWriter* child;
    BSONWriter* parent;

    void enlarge(size_t nbytes)
    {
        uint8_t* out_new = (uint8_t*)realloc(out, (size_t)(pos + nbytes));
        if (out_new == NULL)
        {
            throw "OOM you twat";
        }
        else
        {
            out = out_new;
        }
    }

    char* print_array_name()
    {
        // Windows notes that sprintf_s is available.
        sprintf(array_name, "%d", is_array);
        is_array += 1;
        return array_name;
    }
};

#endif
