db.createUser(
        {
            user: "mongodbuser",
            pwd: "mongodbuserpassword",
            roles: [
                {
                    role: "readWrite",
                    db: "restaurant_app"
                }
            ]
        }
);
db.restaurants.createIndex({restaurants:"2dsphere"})
