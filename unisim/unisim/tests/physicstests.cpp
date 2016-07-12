#include "UnitTest++/UnitTest++.h"
#include "../physics.hpp"
#include "../universe.hpp"
#include "../vector.hpp"

#define ERROR_MARG 0.000000000001
#define NUM_SPECTRUM 5
#define BIG_SPEC_MAG 10

using namespace Diana;

SUITE(Physics)
{
    class PhysicsFixture
    {
    public:
        
        struct Spectrum * big_spectrum;
        struct Spectrum * small_spectrum;
        Universe * myUniverse;
        struct Universe::Parameters myParams;
        
        struct PhysicsObject physObjA, physObjB;
        
        Vector3T< double > zeroVector = {0, 0, 0};
        Vector3T< double > oneVector = {1, 1, 1};
        
        PhysicsFixture ()
        {
            Universe * myUniverse = new Universe(myParams);
            
            big_spectrum = Spectrum_allocate(NUM_SPECTRUM);
            for (int i=0; i<NUM_SPECTRUM; i++)
            {
                (&(big_spectrum->components))[i].wavelength = i;
                (&(big_spectrum->components))[i].power = i;
            }
            
            small_spectrum = Spectrum_allocate(1);
            small_spectrum->components.power = 1;
            small_spectrum->components.wavelength = 1;
            
            
            PhysicsObject_init(&physObjA, myUniverse, &zeroVector, &zeroVector, &zeroVector, &zeroVector, 1.0, 1.0, (char *)"Object A", small_spectrum);
            PhysicsObject_init(&physObjB, myUniverse, &oneVector, &zeroVector, &zeroVector, &zeroVector, 1.0, 1.0, (char *)"Object B", small_spectrum);
        }
    };
    
    TEST_FIXTURE(PhysicsFixture, HugeSpectrumAlloc)
    {
        CHECK_THROW(Spectrum_allocate(0xFFFFFFFF), std::runtime_error);
    }
    
    TEST_FIXTURE(PhysicsFixture, PhysicsObjectTest)
    {
        PhysicsObject * po;
        CHECK_EQUAL((void *)NULL, PhysicsObject_clone(NULL));
        REQUIRE CHECK(PhysicsObject_clone(&physObjA) != (void*)NULL);
    
    }
    
    TEST_FIXTURE(PhysicsFixture, CollisionTest)
    {
        
    }
        
    TEST_FIXTURE(PhysicsFixture, testSpectrum)
    {
        CHECK_CLOSE(total_spectrum_power(big_spectrum), BIG_SPEC_MAG, ERROR_MARG);
        
        //Capture the value, then test against (for regressions)
        //printf ("%0.18f\n", radiates_strong_enough(big_spectrum, 0.0001));
        CHECK_CLOSE(radiates_strong_enough(big_spectrum, 0.01), 79.577471545948, ERROR_MARG);
        CHECK_CLOSE(radiates_strong_enough(big_spectrum, 0.0001), 7957.7471545947673803, ERROR_MARG);
        
        struct Spectrum * newSpectrum = Spectrum_clone(big_spectrum);
        REQUIRE CHECK(newSpectrum != (void *)NULL);
        CHECK_EQUAL(Spectrum_clone(NULL), (void *)NULL);
        CHECK_EQUAL(total_spectrum_power(newSpectrum), total_spectrum_power(big_spectrum));
        
        //run some checks on an invalid spectrum (one with no coponents
        newSpectrum->n = 0;
        CHECK_EQUAL((void *)NULL, Spectrum_clone(newSpectrum));
        CHECK_CLOSE(total_spectrum_power(newSpectrum), 0.0, ERROR_MARG);
        CHECK_CLOSE(radiates_strong_enough(newSpectrum, 1000), 0.0, ERROR_MARG);
        //TODO: after figuring out the rand()
        //CHECK_CLOSE(total_spectrum_power(Spectrum_perturb(newSpectrum, 1.0, 0))), 0.0, ERROR_MARG);
        free(newSpectrum);
        
        newSpectrum = Spectrum_combine(big_spectrum, small_spectrum);
        REQUIRE CHECK(newSpectrum != NULL);
        CHECK_CLOSE(total_spectrum_power(newSpectrum), total_spectrum_power(big_spectrum) + total_spectrum_power(small_spectrum), ERROR_MARG);        
        free(newSpectrum);
        
        newSpectrum = Spectrum_combine(big_spectrum, big_spectrum);
        REQUIRE CHECK(newSpectrum != NULL);
        CHECK_CLOSE(total_spectrum_power(newSpectrum), total_spectrum_power(big_spectrum)*2, ERROR_MARG);        
        free(newSpectrum);

        
        CHECK_CLOSE(total_spectrum_power(small_spectrum), 1.0, ERROR_MARG);        
    }
}



TEST(Sanity)
{
    CHECK_EQUAL(1, 1);
}

int main(int, const char *[])
{
    return UnitTest::RunAllTests();
}