// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include <map>
#include "GameFramework/Actor.h"
#include "ObjectSimConnector.generated.h"

class FSocket;
//class AEventedActor;

USTRUCT(BlueprintType, Blueprintable)
struct FDirectoryItem
{
    GENERATED_USTRUCT_BODY()

        UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Diana Messaging")
        FString name;
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Diana Messaging")
        int32 id;
};

UCLASS()
class EVENTTEST_API AObjectSimConnector : public AActor
{
    friend class FVisDataReceiver;

    GENERATED_BODY()

public:
    struct DianaVDM
    {
        int32 server_id;
        float world_time;
        FVector pos;
    };

    struct DianaActor
    {
        int32 server_id;
        AActor* a;
        float last_time;
        float cur_time;
        FVector last_pos;
        FVector cur_pos;
    };

    // See: https://wiki.unrealengine.com/Multi-Threading:_How_to_Create_Threads_in_UE4
    class FVisDataReceiver : public FRunnable
    {
    public:
        FVisDataReceiver(FSocket* sock, AObjectSimConnector* parent, std::map<int32, struct DianaActor>* oa_map);
        ~FVisDataReceiver();

        virtual bool Init();
        virtual uint32 Run();
        virtual void Stop();

    private:
        FRunnableThread* rt = NULL;
        volatile bool running;
        FSocket* sock = NULL;
        AObjectSimConnector* parent;
        std::map<int32, struct DianaActor>* oa_map;
    };

    // Sets default values for this actor's properties
    AObjectSimConnector();
    ~AObjectSimConnector();

    // Called when the game starts or when spawned
    virtual void BeginPlay() override;

    // Called every frame
    virtual void Tick(float DeltaSeconds) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Server information", meta = (DisplayName = "Server IPv4 Address"))
        FString host = "127.0.0.1";

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Server information", meta = (DisplayName = "Server TCP Port"))
        int32 port = 5506;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Server information", meta = (DisplayName = "Client ID"))
        int32 client_id = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Server information", meta = (DisplayName = "Server ID"))
        int32 server_id = 1;

    //UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Server information", meta = (DisplayName = "Proxy Diana Connector"))
    //    AObjectSimConnector* proxy = NULL;

    UFUNCTION(BlueprintCallable, Category = "Diana Messaging")
        bool RegisterForVisData(bool enable);

    UFUNCTION(BlueprintCallable, Category = "Diana Messaging")
        void UpdateExistingVisDataObject(int32 PhysID, AActor* ActorRef);

    // Don't have access to doubles, or 64-bit ints in Blueprints.
    // See: https://answers.unrealengine.com/questions/98206/missing-support-for-uint32-int64-uint64.html
    UFUNCTION(BlueprintImplementableEvent, Category = "Messages From Diana", meta = (DisplayName = "Received Vis Data Message for New Object"))
        void NewVisDataObject(int32 PhysID, FVector Position);

    UFUNCTION(BlueprintImplementableEvent, Category = "Messages From Diana", meta = (DisplayName = "Received Vis Data Message for Existing Object"))
        void ExistingVisDataObject(int32 PhysID, FVector CurrentPosition, FVector LastPosition, float CurrentRealTime, float LastRealTime, AActor* ActorRef);

    UFUNCTION(BlueprintCallable, Category = "Diana Messaging")
        TArray<struct FDirectoryItem> DirectoryListing(FString type, TArray<struct FDirectoryItem> items);

    UFUNCTION(BlueprintCallable, Category = "Diana Messaging")
        void CreateShip(int32 class_id);

    UFUNCTION(BlueprintCallable, Category = "Diana Messaging")
        void JoinShip();

    UFUNCTION(BlueprintCallable, Category = "Diana Messaging")
        void RenameShip(FString NewShipName);

    UFUNCTION(BlueprintCallable, Category = "Diana Messaging")
        void Ready();

protected:
    TArray<struct FDirectoryItem> DirectoryListing(int32 client_id, int32 server_id, FString Type, TArray<struct FDirectoryItem> Items);
    void CreateShip(int32 client_id, int32 server_id, int32 class_id);
    void JoinShip(int32 client_id, int32 server_id);
    void RenameShip(int32 client_id, int32 server_id, FString NewShipName);
    void Ready(int32 client_id, int32 server_id);

private:
    FVisDataReceiver* vdr_thread = NULL;
    bool ConnectSocket();
    void DisconnectSocket();
    FSocket* sock = NULL;

    // See: http://www.slideserve.com/maine/concurrency-parallelism-in-ue4
    TQueue<struct DianaVDM> messages;

    // See: https://answers.unrealengine.com/questions/207675/fcriticalsection-lock-causes-crash.html
    FCriticalSection map_cs;
    std::map<int32, struct DianaActor>::iterator it;
    std::map<int32, struct DianaActor> oa_map;
};
