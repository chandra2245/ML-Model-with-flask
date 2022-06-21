


function d3CallsLineGraph(data,divid) {
  // set the dimensions and margins of the graph
var linediv=d3.select("#"+divid);



var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = parseInt(linediv.style("width")) - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

// parse the date / time
var parseTime = d3.timeParse("%d-%b-%y");

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);



// define the line
var callsline = d3.line()
    .curve(d3.curveCardinal)
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.calls); });
	

	

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("#"+divid).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
            .attr("transform",
             "translate(" + margin.left + "," + margin.top + ")");

  const tooltipLine = svg.append('line');	
	
  //tooltip		  
  let tooltip = d3.select('body').append('div')
     .attr('class', 'tooltips')
     .attr('id',"tooltip"+divid);

  // format the data
  data.forEach(function(d) {
      d.date = parseTime(d.date);
      d.calls = +d.calls;

  });

  // Scale the range of the data
  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0,300+ d3.max(data, function(d) 
      { 
     	  return d.calls;})]);


	   


    // Data line and dots group
    var lineAndDots = svg.append("g")
    		.attr("class", "line-and-dots")


    // Data line
    lineAndDots.append("path")
        .datum(data)
        .attr("class", "data-line")
        .attr("d", callsline);

    // Data dots
    lineAndDots.selectAll("line-circle")
    		.data(data)
    	.enter().append("circle")
        .attr("class", "data-circle")
        .attr("r", 5)
        .attr("cx", function(d) { return x(d.date); })
        .attr("cy", function(d) { return y(d.calls); });
       		
     svg.selectAll(".text")  		
	  .data(data)
	  .enter()
	  .append("text")
	  .attr("class","label")
	  .attr("x", (function(d) { return x(d.date)-10  ; }  ))
	  .attr("y", function(d) { return y(d.calls) -20; })
	  .attr("dy", ".75em")
	  .text(function(d) { return d.calls; });  
	  
  // Add the X Axis
  svg.append("g")
      .attr("class", "axisCSS")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat("%d-%b")))   
      .selectAll("text")	
        .style("text-anchor", "middle")
		 .attr("class","xlabelbar");
      
  // Add the Y Axis
 // svg.append("g")
  //    .call(d3.axisLeft(y));
	  
var  tipBox = svg.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('opacity', 0)
    .on('mousemove', drawTooltip)
    .on('mouseout', removeTooltip);
	  
  function removeTooltip() {
    tooltip.style('display', 'none');
	tooltipLine.attr('stroke', 'none');
  }
  
    function drawTooltip() {
	  var year = new Date(x.invert(d3.mouse(tipBox.node())[0]));
       year.setDate(year.getDate()-3);

	  var year2 = x.invert(d3.mouse(tipBox.node())[0]);
      var actual_s=0;


    for (i in data) {
             if(data[i].date>=year){
                year2=data[i].date;
                actual_s=data[i].calls;
                break;
           } 
         }
	  



    tooltipLine.attr('stroke', 'black')
    .attr('x1', x(year2))
    .attr('x2', x(year2))
    .attr('y1', 0)
    .attr('y2', height);
  
       tooltip.style('left', (d3.event.pageX+10) + 'px')
       .style('top', (d3.event.pageY-10) + 'px')
      .style('display', 'inline-block')
	  .html("Date: "+GetFormattedDate(year2)+"<br>Calls: "+actual_s);
  }
  



 
  
}


function GetFormattedDate(year2) {
    var todayTime = year2;
    var month = todayTime.getMonth() + 1;
    var day = todayTime.getDate();
    var year = todayTime.getFullYear();
    return day + "/" + month + "/" + year;
}