const express = require('express')
const router = express.Router();

router.get('/',(req,res,next)=>{
  const spawn = require('child_process').spawn;
  const result = spawn('python',['contents-based-filtering.py',''])
  result.stdout.on('data', function(data) {
    console.log("!!!!!!!!!!!!!!!!!!data.toString()");
  });
  res.json([{id:1,username:'daisy'}])
})