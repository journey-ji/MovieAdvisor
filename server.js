const express = require('express')
const { Server } = require('http')
const path = require('path')
const movieRouter = require('./frontend/static/js/moives.js')
const app = express()


app.use(express.static('public'))
// static 폴더를 정적파일 제공을 위해 사용
app.use('/static',express.static(path.resolve(__dirname,'frontend','static')))

app.use('/movies',movieRouter)

app.get('/*',(req,res)=>{
  res.sendFile(path.resolve('frontend','index.html'))
})



app.listen(process.env.PORT || 3000, ()=>console.log(`Server running on 3000`))

