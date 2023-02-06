class Wheel {

  constructor(wheel) {
    this.wheel = wheel;
    this.originalPos = wheel.getBoundingClientRect()
    this.centerX = this.originalPos.left + (this.originalPos.width)/2
  	this.centerY = this.originalPos.top + (this.originalPos.height)/2
  }

  rotate(degrees) {
    this.wheel.style.transform = 'rotate('+degrees+'deg)';
  }

  findSlope(x2, y2){
  	return  ((y2 - this.centerY)/(x2-this.centerX))  	
  }

  determineAngleToBeRotated(event){
  
  	if((event.clientY < this.centerY) && (event.clientX!=this.centerX)){
  		var angleInDegrees = 	(Math.atan(this.findSlope(event.clientX, event.clientY))) * 180 / Math.PI
  		this.rotate(angleInDegrees > 0 ? -(90-Math.abs(angleInDegrees)) : (90-Math.abs(angleInDegrees)))
  	}
  }
}

class Car{
  constructor(stopResumeToggler){
    this.stopResumeToggler  = stopResumeToggler
  }
  stop(){
    this.stopResumeToggler.innerText = "Resume"
    this.stopResumeToggler.onclick = () => this.resume()
  }
  resume(){
    this.stopResumeToggler.innerText = "Stop"
    this.stopResumeToggler.onclick = () => this.stop()
  }
}