var mongoose = require("mongoose");
var gameSchema = new mongoose.Schema({
    gameName: String,
    platform: [String],
    originalPrice: Number,
    discountedPrice: [{
      date: Date,
      price: Number
    }]
});

module.exports = mongoose.model("Game", gameSchema);
