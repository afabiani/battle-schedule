// CEST (Central European Summer Time) is one of the well-known names of UTC+2 time zone which is 2h
var offsetCETTime = '+02:00'; 

// Main page load function starts here
$(function() { 
    // First set the offset time in string
    setCETOffsetTime();

    // Get difference in number of days - start date to today - CET
    var _daysDifference = getDayDifference();

    var dayNumber = 1;
    // Formulae - get the total no of days difference and divide it by 11 and take the reminder
    // Example - 23/11 = 1 (reminder) 
    if(_daysDifference < 11) { 
        if(_daysDifference == 0) { 
            dayNumber = 0;
        } else { 
            dayNumber = _daysDifference;
        }
    } else { 
        // Divide by 11
        // If reminder is 0, then its index is 11, the last scheduled day.
        var reminder = _daysDifference % 11; 
    
        dayNumber = reminder;
    }
    console.log("Difference :" + _daysDifference + " / Day index :" + dayNumber);

    // Set the card data
    $("#spDay").html(schedules.data[dayNumber].day);
   
    // All table creation goes below
    createDataTables(dayNumber);

    // Refresh every 1 second
    // setTimeout(updateTime, 1000);
    setInterval(function() { updateTime(dayNumber);}, 1000);
});
   

function setCETOffsetTime() {
    var isDST =false;
    var today = new Date();
    if (today.isDstObserved()) { 
        isDST = true;
    }

    if(!isDST){
        // During the winter, CET - Central European Time(UTC+1) is in use
        offsetCETTime = '+01:00';
    }
}


function getDayDifference() {
    var _start = moment.tz(new Date("2020-11-06"), "Europe/Amsterdam").format('YYYY-MM-DD');
    var _today = moment.tz(new Date(), "Europe/Amsterdam").format('YYYY-MM-DD');

    var _s = moment(_start);
    var _t = moment(_today);

    var duration = moment.duration(_t.diff(_s));
    var _daysDifference = duration.asDays();

    // If negative, convert it to positive
    _daysDifference = _daysDifference < 0 ? _daysDifference * -1 : _daysDifference;
    
    // console.log("Days diff: " + _daysDifference)
    return _daysDifference;
}   


function createDataTables(dayNumber) {
    // Get events data for the day
    _data = schedules.data[dayNumber].info;
    _main = createTable(_data, "today", "today", true);
   
    // Get events data for the next day
    if(dayNumber > 9) { 
        dayNumber = 0;
    } else { 
        dayNumber += 1;
    }

    _data = schedules.data[dayNumber].info;
    _main += createTable(_data, "tomorrow", "tomorrow", false);
   
    // Get events data for the day after
    if(dayNumber > 9) { 
        dayNumber = 0;
    } else { 
        dayNumber += 1;
    }

    _data = schedules.data[dayNumber].info;
    _main += createTable(_data, "day after", "tomorrow", false);
   
    // Populate the table
    $("#eventsTable").html(_main);
}


function updateTime(){ 
    // console.log("Offset Time: " + offsetCETTime);
    var _utcUTC = moment.utc(new Date());
    _utcUTC1 = _utcUTC.format('MMM DD hh:mm:ss A');
    var _utcCEST = moment.utc(new Date()).utcOffset(offsetCETTime);
    _utcCEST1 = _utcCEST.format('MMM DD hh:mm:ss A');

    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const currentTime = moment().tz(timezone).format('MMM DD hh:mm:ss A');

    // Set UTC and Local time
    $("#spUTC").html(_utcUTC1);
    $("#spCET").html(_utcCEST1);
    $("#spLocal").html(currentTime);

    // Highlight the event cells which are happening now in CET timezone
    _times = _utcCEST.format('hh A').split(" ");
    _currentHour = _times[0];
    _currentDay = _times[1];
    // console.log(_times);

    // Intialize current time-event arrays
    _event0 = [12, 1, 2, 3, 4, 5];
    _event0A = "AM";
    _event1 = [6, 7, 8, 9, 10, 11];
    _event1A = "AM";
    _event2 = [12, 1, 2, 3, 4, 5];
    _event2A = "PM";
    _event3 = [6, 7, 8, 9, 10, 11];
    _event3A = "PM";
    

    // Enable the correct color bg for cells based on time of happening event
    if(_event0.indexOf(parseInt(_currentHour)) != -1 && _currentDay == _event0A) { 
        $(".event0").css("background-color", "#beffcf");
    } else if (_event1.indexOf(parseInt(_currentHour)) != -1 && _currentDay == _event1A) { 
        $(".event1").css("background-color", "#beffcf");
    } else if (_event2.indexOf(parseInt(_currentHour)) != -1 && _currentDay == _event2A) { 
        $(".event2").css("background-color", "#beffcf");
    } else if (_event3.indexOf(parseInt(_currentHour)) != -1 && _currentDay == _event3A) { 
        $(".event3").css("background-color", "#beffcf");
    }
    console.log("In CET - Hour: " + _currentHour + " / Day :" + _currentDay);
}

   
function stdTimezoneOffset() {
    var _CET = moment.tz("2013-12-01", "Europe/Amsterdam").format('Z');
    var _CEST = moment.tz("2013-06-01", "Europe/Amsterdam").format('Z');

    _timeCET = parseInt(_CET.split(':')[0]);
    _timeCEST = parseInt(_CEST.split(':')[0]);
    return Math.max(_timeCET, _timeCEST);
}


Date.prototype.isDstObserved = function () {
    var currentEuropeanTimeOffset = moment.tz(new Date(), "Europe/Amsterdam").format('Z z');
    _timeEUR = parseInt(currentEuropeanTimeOffset.split(':')[0]);
    return currentEuropeanTimeOffset < stdTimezoneOffset();
}


function createTable(data, txt, cssclass, hlight) { 
    _headerRow = addHeaderRow(_data, hlight);
    _dataRow = addDataRow(_data, hlight);

    // Construct the final table data
    _main = "<div class='subtblHdr'>"+ txt + "</div>";
    _main += "<table class='eventTbl " + cssclass + "'>"+ _headerRow + _dataRow + "</table><br/>";

    return _main;
}
   
   
function addHeaderRow(info, hlight) { 
    _times = info.time;
    var _htmlText = "<tr class='tblHeader'>";
    for(i in _times) { 
        if(hlight) { 
            _htmlText += "<td class='" + "event" + i.toString() + "'>" + _times[i] + "</td>";
        } else { 
            _htmlText += "<td>" + _times[i] + "</td>";
        }
    }
    _htmlText += "</tr>";

    return "<thead>" + _htmlText + "</thead>";
}
   

function addDataRow(info, hlight) { 
    events = info.events;
    var _htmlText = "";

    for(i in events) { 
        eventsLen = events[i].length;
        _data = events[i];
        _row = "<tr>";
        for(var j=0; j<eventsLen; j++) { 
            if(hlight) { 
                if(i == 1) {
                    if(j == 0 || j == 3) {
                        _row += "<td class='" + "event" + j.toString() + " hour12two'>" + _data[j] + "</td>"; 
                    } else if(j == 1 || j == 2) {
                        _row += "<td class='" + "event" + j.toString() + " hour12one'>" + _data[j] + "</td>"; 
                    }
                } else {
                    _row += "<td class='" + "event" + j.toString() + "'>" + _data[j] + "</td>"; 
                }
            } else { 
                _row += "<td>" + _data[j] + "</td>"; 
            }
        }
        _row += "</tr>";
        _htmlText += _row;
    }

    return "<tbody>" + _htmlText + "</tbody>";
}