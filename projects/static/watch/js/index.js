     setInterval(()=>{
        let d = new Date();
        let hours = d.getHours(); 
        let minutes = d.getMinutes();
        let seconds = d.getSeconds();
       
        let time = document.getElementById("time");
        let second = document.getElementById("second");
        let minute = document.getElementById("minute");
        let hour = document.getElementById("hour");
        let secondangel = seconds * 6;
        let minute_angel = minutes * 6 ;
        let hour_angel = hours * 6;
        if (hours > 12 ){
            hour_angel = (hours - 12)*30 + (minutes * 0.5);
        }else{
            hour_angel = (hours)*30;
        }            
        if (seconds < 10){
            seconds = `0${seconds}`
        }
        if (minutes < 10){
            minutes = `0${minutes}`
        }
        if (hours < 10){
            hours = `0${hours}`
        }
        // time.innerHTML=`${hours}:${minutes}:${seconds}`
        second.style.transform=`rotate(${secondangel}deg)`
        minute.style.transform=`rotate(${minute_angel}deg)`
        hour.style.transform=`rotate(${hour_angel}deg)`       

     }, 1000); 

    