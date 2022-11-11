




document.addEventListener('click',e=>{
  let handle 
  if(e.target.matches(".handle")) handle = e.target
  else {
    handle = e.target.closest('.handle')
  }
  if(handle !== null){
    onHandleClick(handle)
  }
})

window.addEventListener('resize',(e)=>{
  // progress bar 크기 재설정
})

document.querySelectorAll(".progress-bar").forEach(calculateProgressBar)

function calculateProgressBar(progressBar){
  progressBar.innerHTML = ''
  const slider =progressBar.closest(".row").querySelector(".slider")
  console.log(slider)
  
  const itemCount = slider.children.length
  const itemsPerScreen = parseInt(getComputedStyle(slider).getPropertyValue('--items-per-screen'))
  const sliderIndex = parseInt(getComputedStyle(slider).getPropertyValue('--slider-index'))

  // img수 / 화면당 item수ㅜ
  const progressBarItemCount = Math.ceil(itemCount/itemsPerScreen)
  for(let i=0; i<progressBarItemCount;i++){
    const barItem = document.createElement('div')
    barItem.classList.add("progress-item")
    if(i===sliderIndex){
      barItem.classList.add('active')
    }
    progressBar.append(barItem)
  }
}

function onHandleClick(handle){
  const progressBar = handle.closest('.row').querySelector('.progress-bar')
  const slider = handle.closest('.cont-trending').querySelector(".slider")
  const sliderIndex = parseInt(
    getComputedStyle(slider).getPropertyValue('--slider-index'))

  const progressBarItemCount = progressBar.children.length
  if(handle.classList.contains("left-handle")){
    if(sliderIndex <=0){
      slider.style.setProperty('--slider-index',progressBarItemCount-1)
      progressBar.children[sliderIndex].classList.remove('active')
      progressBar.children[progressBarItemCount-1 ].classList.add('active')
    }else{
      slider.style.setProperty('--slider-index',sliderIndex -1)
      progressBar.children[sliderIndex].classList.remove('active')
      progressBar.children[sliderIndex -1 ].classList.add('active')
    }

  }
  if(handle.classList.contains("right-handle")){
    if(sliderIndex +1  >= progressBarItemCount){
      slider.style.setProperty('--slider-index',0)
      progressBar.children[sliderIndex].classList.remove('active')
      progressBar.children[0].classList.add('active')
    }else{
      slider.style.setProperty('--slider-index',sliderIndex +1)
      progressBar.children[sliderIndex].classList.remove('active')
      progressBar.children[sliderIndex +1 ].classList.add('active') 
    }
  }
  
}