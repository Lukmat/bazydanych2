import express from 'express'
import {connectToServer, getDb} from "./mongo";
import {ObjectId} from "mongodb";


const app = express()
const port = 3000

app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
})

const products = "products"

connectToServer(() => {
    console.log("Connected to MongoDB server")
})

app.get('/products', (req, res) => {
    getDb().collection(products).find({}).toArray().then((result) => {
        res.send(result)
    }).catch((err) => {
        res.status(500).send(err)
    })
})

app.post('/products/create/:name/:price/:quantity', (req, res) => {
    const name = req.params.name
    const price = parseFloat(req.params.price) 
    const quantity = parseInt(req.params.quantity) 

    const obj = {
        name: name,
        price: price,
        quantity: quantity
    }

    getDb().collection(products).insertOne(obj).then((result) => {
        res.send(result)
    }).catch((err) => {
        res.status(500).send(err)
    })
})

app.put('/products/:id', (req, res) => {
    const id = req.params.id
    const price = req.query.price
    const name = req.query.name
    const quantity = req.query.quantity

    const updates = {}

    if(price){
        updates.price = price
    }

    if(name){
        updates.name = name
    }

    if(quantity){
        updates.quantity = quantity
    }

    getDb().collection(products).findOneAndUpdate({_id: new ObjectId(id)}, {$set: updates}, {returnOriginal: false})
        .then((result) => {
            if(!result.value) {
                res.status(404).send("Product not found")
            }
            else {
                res.send(result.value)
            }
        })
        .catch((err) => {
            res.status(500).send(err)
        })
})


app.delete('/products/:id', (req, res) => {
    const id = req.params.id

    getDb().collection(products).findOneAndDelete({_id: new ObjectId(id)}).then((result) => {
        if(!result.value) {
            res.status(404).send("Product not found")
        }
        else {
            res.send(result.value)
        }
    }).catch((err) => {
        res.status(500).send(err)
    })
})


app.get('/products/generateReport', (req, res) => {
    getDb().collection(products).aggregate([
        {
            $group: { _id: "$name", ilosc: { $sum: "$quantity" }, wartosc: {$sum: {$multiply: [ "$price", "$quantity" ]}}}
        }
    ]).toArray().then((result) => {
        res.send(result)
    }).catch((err) => {
        res.status(500).send(err)
    })
})
