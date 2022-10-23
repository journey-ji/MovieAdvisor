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

let movieList =[]
app.post('/test', function(req, res) {
  var name = req.body.name;
  var price = req.body.price;
  movieList.push(req.body.movieId)
  console.log("Is send it?");
  console.log(name + " " + price);
  res.status(200).json({1: name, 2:price,3:movieList})
})


exports.testData



// 진행사항
// 
// 1. 콘텐츠기반 필터링에 선호항목 추가하고 이를 바탕으로 코사인 유사도 구하기
// 2. 포스터 누르면 해당 영화를 서버로 넘겨서 파이썬의 선호항목에 추가하기
// 3. 
// 
// 
// 
