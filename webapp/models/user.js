const mongoose = require('mongoose');
const passportLocalMongoose = require('passport-local-mongoose');

const UserSchema = new mongoose.Schema({
  username: String,
  password: String,
  games: [{
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Game"
    },
    desiredPrice: Number
  }]
});

UserSchema.plugin(passportLocalMongoose);

module.exports = mongoose.model('User', UserSchema);
