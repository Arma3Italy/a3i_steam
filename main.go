package main

import (
	"context"
	"fmt"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Users struct {
	Name    string
	SteamID string
	Url     string
	Avatar  string
}

func main() {
	clientOptions := options.Client().ApplyURI("mongodb+srv://admin:admin@arma3italy-eufgo.mongodb.net/test2")
	client, _ := mongo.Connect(context.TODO(), clientOptions)

	collection := client.Database("test").Collection("users")
	filter := bson.D{{"steamid", "76561198141770676"}}

	// update := bson.D{{"$set", bson.D{
	// 	{"armahours", "11111"},
	// }}}
	// updateResult, _ := collection.UpdateOne(context.TODO(), filter, update)

	var result Users
	_ = collection.FindOne(context.TODO(), filter).Decode(&result)
	fmt.Printf("%+v", result.Name)

	_ = client.Disconnect(context.TODO())
}
