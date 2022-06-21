


function d3LineGraph(data,divid) {
  // set the dimensions and margins of the graph
var linediv=d3.select(divid);



var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = parseInt(linediv.style("width")) - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

// parse the date / time
var parseTime = d3.timeParse("%d-%b-%y");

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);



// define the line
var actual_salesline = d3.line()
    .curve(d3.curveCardinal)
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.actual_sales); });
	
var target_salesline = d3.line()
    .curve(d3.curveCardinal)
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.target_sales); });
	

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select(divid).append("svg")
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
      d.actual_sales = +d.actual_sales;
	  d.target_sales= +d.target_sales;
  });

  // Scale the range of the data
  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) 
      { if (d.actual_sales> d.target_sales)
     	  return d.actual_sales;
        else 
		  return d.target_sales; })]);


	   
 // Add the actual_salesline path.
  let l1 = svg.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", actual_salesline)
	  .attr("stroke","#C33469");
	  
 // Add the target_salesline path.
  let l2=svg.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", target_salesline)    	  
	  .attr("stroke","#346DC3");
       		
 
	  
  // Add the X Axis
  svg.append("g")
      .attr("class", "axisCSS")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat("%d-%b")));

  // Add the Y Axis
  svg.append("g")
      .attr("class", "axisCSS")
      .call(d3.axisLeft(y));
	  
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
	  const year = x.invert(d3.mouse(tipBox.node())[0]);
       year.setDate(year.getDate()-3);

	  var year2 = x.invert(d3.mouse(tipBox.node())[0]);
      var actual_s=0;
	  var target_s=0;
	  console.log(year);
	  
	  for (i in data) {
             if(data[i].date>=year){
                year2=data[i].date;
                actual_s=data[i].actual_sales;
				target_s=data[i].target_sales;
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
	  .html("Date: "+GetFormattedDate(year2)+"<br>Actual Sales: "+actual_s+"<br>Target Sales: "+target_s);
  }
  
  		  
  svg.append("circle").attr("cx",width-100).attr("cy",10).attr("r", 6).style("fill", "#C33469")
  svg.append("circle").attr("cx",width-100).attr("cy",35).attr("r", 6).style("fill", "#346DC3")
  svg.append("text").attr("x", width-80).attr("y", 10).text("Actual Sales").style("font-size", "15px").attr("alignment-baseline","middle")
  svg.append("text").attr("x", width-80).attr("y", 35).text("Target Sales").style("font-size", "15px").attr("alignment-baseline","middle")

 
  
}


function GetFormattedDate(year2) {
    var todayTime = year2;
    var month = todayTime.getMonth() + 1;
    var day = todayTime.getDate();
    var year = todayTime.getFullYear();
    return day + "/" + month + "/" + year;
}