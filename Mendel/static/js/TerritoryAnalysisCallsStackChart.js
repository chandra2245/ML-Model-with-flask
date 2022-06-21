


function d3CallsStackGraph(data,divid,statusArray) {
  // set the dimensions and margins of the graph
var linediv=d3.select("#"+divid);

var margin = {top: 0, right: 20, bottom: 30, left: 50},
    width = parseInt(linediv.style("width")) - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

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

// parse the date / time
var parseTime = d3.timeParse("%d-%b-%y");

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

var color = d3.scaleOrdinal(d3.schemeCategory10);

//var statusArray = ['BRANDED','UNBRANDED'];

//var statusArray = ['High','Medium','Low','Non Target'];


    var parsedData = data.map(function (d) {
      var dataObject = {
        date: parseTime(d.date)
      };
      statusArray.forEach(function (s) {
        dataObject[s] = +d[s];
      })
      return dataObject;
    });





   var stack = d3.stack()
      .keys(statusArray)
      .offset(d3.stackOffsetNone)
      ;

    var layers = stack(parsedData);

    function getDate(d) {
      return d.date;
    }
// define the line
    var x = d3.scaleTime()
      .domain([parsedData[0].date, parsedData[parsedData.length - 1].date])
      .range([0, width]);

    var y = d3.scaleLinear()
      .domain([0, d3.max(layers, stackMax)])
      .range([height, 0]);

    var xAxis = d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat("%d-%b")),
      yAxis = d3.axisLeft(y);

    var gX = svg.append("g")
      .attr("class", "axisCSS")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text")	
        .style("text-anchor", "middle")
		 .attr("class","xlabelbar")
      .select(".domain")
      .remove();

    //var gY = svg.append("g")
    //  .attr("class", "axis axis--y")
    //  .call(yAxis);

    var colors = statusArray.map(function (d, i) {
      return d3.interpolateWarm(i / statusArray.length);
    });

    var colorScale = d3.scaleOrdinal()
      .domain(statusArray)
      .range(colors);

    var legendOffset = margin.left-120 + width - 80 * statusArray.length;

    var legend = d3.legendColor()
      .shapeWidth(80)
      .cells(statusArray.length)
      .orient("horizontal")
      .scale(colorScale)

    var area = d3.area()
      .x(function (d, i) { return x(d.data.date) })
      .y0(function (d) { return y(d[0]); })
      .y1(function (d) { return y(d[1]); })
      .curve(d3.curveBasis);

    var layerGroups = svg.selectAll(".layer")
      .data(layers)
      .enter().append("g")
      .attr("class", "layer");

    svg.append("g")
      .attr("class", "legend")
      .attr("transform", "translate(" + legendOffset.toString() + ",0)");

    svg.select(".legend")
      .call(legend);

    layerGroups.append("path")
      .attr("d", area)
      .attr("fill", function (d, i) {
        return colors[i];
      });

    function stackMax(layer) {
      return d3.max(layer, function (d) { return d[1]; });
    }  

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

    var str="";
    for (i in parsedData) {
             if(parsedData[i].date>=year){
                year2=parsedData[i].date;
                statusArray.forEach(function (s) {
                      str=str.concat('<br>',s,' : ',parsedData[i][s]);
                })
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
	  .html("Date: "+GetFormattedDate(year2)+str);
  }
  

}



function GetFormattedDate(year2) {
    var todayTime = year2;
    var month = todayTime.getMonth() + 1;
    var day = todayTime.getDate();
    var year = todayTime.getFullYear();
    return day + "/" + month + "/" + year;
}