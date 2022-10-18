const express = require('express')
const { Server } = require('http')
const path = require('path')
const app = express()
const {spawn} = require('child_process');

app.use(express.static('public'))
// static 폴더를 정적파일 제공을 위해 사용
app.use('/static',express.static(path.resolve(__dirname,'frontend','static')))

let testData;
app.get('/test',(req,res)=>{
  let dataToSend;
  const python = spawn('python3', ['contents-based-filtering.py']);
  python.stdout.on('data', (data) => {
    dataToSend = data.toString()
    testData = dataToSend
    console.log(dataToSend)
    console.log("END!")
  })
  python.on('close', (code) => {
     res.json(dataToSend);
  })
})


app.get('/*',(req,res)=>{
  res.sendFile(path.resolve('frontend','index.html'))
})



app.listen(process.env.PORT || 3000, ()=>console.log(`Server running on 3000`))

exports.testData



// 진행사항
// 
// 1. 콘텐츠기반 필터링에 선호항목 추가하고 이를 바탕으로 코사인 유사도 구하기
// 2. 포스터 누르면 해당 영화를 서버로 넘겨서 파이썬의 선호항목에 추가하기
// 3. 
// 
// 
// 
// 
// 
// 
// 
// 
// 
