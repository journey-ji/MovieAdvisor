const express = require('express');

const router = express.Router();



        
/* GET home page. */
router.get('/', function(req, res, next) {
  console.log('hi')
  const spawn = require('child_process').spawn;
  const result = spawn('python', ['../../contents-based-filtering.py']);
  result.stdout.on('data',(result)=>{
      console.log(data.toString())
  })
  console.log('index.js')
  res.sendFile(__dirname+'/../public/index.html');
});

module.exports = router;
