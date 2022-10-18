var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
const { createServer } = require('http');

var app = express();
const server = createServer(app);
const cors = require('cors')
const PORT = 8080;
let corsOptions = {
  origin:'',
  credentials: true,
}
app.use(cors(corsOptions))


server.listen(PORT,()=>{
  console.log(`Server running on ${PORT}`);
  
  const spawn = require('child_process').spawn;
  
  const result = spawn('python3', ['ind.py']);
  result.stdout.on('data',(result)=>{
      console.log(data.toString())
  })
})
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
