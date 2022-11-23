const express = require('express')
const { Server } = require('http')
const path = require('path')
const app = express()
const {spawn} = require('child_process');


// 아래부터 세줄 json데이터 참조를 위해 필요
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// static 폴더를 정적파일 제공을 위해 사용
app.use(express.static('public'))
app.use('/static',express.static(path.resolve(__dirname,'frontend','static')))
app.use('/node_modules',express.static(path.join(__dirname,'/node_modules')))


// cors 정책 피하기1
const cors = require('cors')
app.use(cors());


const mongoose = require('mongoose')
const db = mongoose.connection
const dbConfig = require('./config/dbConfig.json')
db.on('error',console.error)
db.once('open',()=>{
  console.log('db서버가 연결되었습니다.')
})
mongoose.connect(
  `mongodb+srv://gentleking95:${dbConfig.pw}@movieadvisor.pvqkw70.mongodb.net/?retryWrites=true&w=majority`,
  {useNewUrlParser: true,useUnifiedTopology:true}
)


/*
날씨관련하여 ,,, 데이터를 받아오는 방법 2가지,,, 

1. 파이썬파일 두개로 각자만들고, fetch 2번해서 하나는 추천영화, 하나는 날씨관련영화 가져오기
2. 파이썬파일 하나에 때려박아서, fetch 1번만하고 데이터를 통째로 받아와서, 파싱해서 나눠쓰기

.. 1번하면 귀찮아 다시만들어야함 근데 버그는 안날듯
2번하면 원래있던 파이썬 파일이랑, server, client 파일 다고쳐야하는데 ,,,
갑자기 버그나면 빡칠듯


1번 ㄱㄱ

to do list
1. 날씨관련 추천하는 파이썬 프로그램 제작
2. server에서 파이썬 프로그램 데이터 가져오기 
3. client - server 연결하기 


*/ 



app.get('/test',(req,res)=>{
  let dataToSend;
  const python = spawn('python3', ['contents-based-filtering2.py',[109445]]);
  python.stdout.on('data', (data) => {
    dataToSend = data.toString()
    testData = dataToSend
  })
  python.on('close', (code) => {
     res.json(dataToSend);
  })
})





app.get('/weather',(req,res)=>{
  let dataToSend;
  const python = spawn('python3', ['weather-based-recom.py','rain']);
  python.stdout.on('data', (data) => {
    dataToSend = data.toString()
    testData = dataToSend
  })
  python.on('close', (code) => {
     res.json(dataToSend);
  })
})


app.get('/*',(req,res)=>{
  res.sendFile(path.resolve('frontend','index.html'))
})

app.listen(process.env.PORT || 3000, ()=>console.log(`Server running on 3000`))



let movieList =[]
app.post('/test', async function(req, res) {
  if(movieList.length>=7){
    movieList.shift()
  }
  movieList.push(parseInt(req.body.movieId))
  console.log(movieList)

 
  let dataToSend
  const python =  await spawn('python3',['contents-based-filtering2.py',movieList])
  python.stdout.on('data',(data)=>{
    dataToSend = data.toString()
    testData = dataToSend
  })
  python.on('close',  (code) => {
    res.json(dataToSend);
  })
  
})

app.post('/weather',async function(req,res){
  let dataToSend;
  weather = req.body.weather
  const python = await spawn('python3', ['weather-based-recom.py',weather]);
  python.stdout.on('data', (data) => {
    dataToSend = data.toString()
    testData = dataToSend
    console.log(dataToSend)
  })
  python.on('close', (code) => {
     res.json(dataToSend);
  })
})


app.get('/weather',(req,res)=>{
  let dataToSend;
  weather = 'sunny'//req.body.weather
  const python = spawn('python3', ['weather-based-recom.py',weather]);
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
exports.testData



// 진행사항
// 10.24일 파이썬 연동부분 비동기처리 완료 

// 11.03일 추천영화리스트 7개로 제한하기 완료

// 