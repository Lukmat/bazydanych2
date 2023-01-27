import {MongoClient} from "mongodb";

const connectionString = "mongodb://localhost:27017/"


const client = new MongoClient(connectionString, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

let dbConnection;

export function connectToServer(callback) {
    client.connect(function (err, db) {
        if (err || !db) {
            return callback(err);
        }

        dbConnection = db.db("db3");
        console.log("Successfully connected to MongoDB.");

        return callback();
    });
}

export function getDb() {
    return dbConnection;
}