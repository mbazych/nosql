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
db.restaurants.createIndex({location:"2dsphere"})
