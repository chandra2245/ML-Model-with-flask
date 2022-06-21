

function d3ParetoChart(data,chartID) { 

    var   paretodiv=d3.select("#"+chartID);
    

 
  var m = {top: 10, right: 70, bottom: 140, left: 50}
  , h = 450 - m.top - m.bottom
  , w = parseInt(paretodiv.style("width")) - m.left - m.right
  , barWidth = 1
  ,misc = {ylabel: 7, xlabelH : 5, title:11}
  ,color = d3.scaleOrdinal(d3.schemeCategory10);
  
  
  var dataset = null;
  
var totalAmount = 0;
  for(var i = 0; i < data.length; i++){
    data[i].Amount = +data[i].Amount;
    totalAmount += data[i].Amount;
    if(i > 0){
      data[i]['CumulativeAmount'] = data[i].Amount + data[i-1].CumulativeAmount;
    }else{
      data[i]['CumulativeAmount'] = data[i].Amount;
    }
  }
  //now calculate cumulative % from the cumulative amounts & total, round %
  for(var i = 0; i < data.length; i++){
    data[i]['CumulativePercentage'] = ((data[i]['CumulativeAmount'] / totalAmount)*100);
    data[i]['CumulativePercentage'] = parseFloat(data[i]['CumulativePercentage'].toFixed(2));
  }
  var Horline=null;
  var Horper=null;
  for(var i = 0; i < data.length; i++){
    if(data[i]['CumulativePercentage']>=80){
	Horline=data[i]['Category'];
	Horper=data[i]['CumulativePercentage'];
	break;
    }
  }

  
  dataset = data;
  
  
  
  let tooltip = d3.select('body').append('div')
  .attr('class', 'tooltips')
  .attr('id',"tooltip"+chartID);
  
  
  //Axes and scales
  var xScale = d3.scaleBand().rangeRound([0, w]).padding(0.1);
  xScale.domain(data.map(function(d) { return d.Category; }));

  var yhist = d3.scaleLinear()
                  .domain([0, d3.max(data, function(d) { return d.Amount; })])
                  .range([h, 0]);

  var ycum = d3.scaleLinear().domain([0, 100]).range([h, 0]);

  var xAxis = d3.axisBottom(xScale);
 
  var yAxis = d3.axisLeft(yhist);


  var yAxis2 = d3.axisLeft(ycum);
 

  //Draw svg
  var svg = d3.select("#"+chartID).append("svg")
              .attr("width", w + m.left + m.right)
              .attr("height", h + m.top + m.bottom)
              .append("g")
              .attr("transform", "translate(" + m.left + "," + m.top + ")");
			  

		  

  //Draw barchart
  var bar = svg.selectAll(".bar")
                .data(data)
                .enter().append("g")
                .attr("class", "bar");

  bar.append("rect")
      .attr("x", function(d) { return xScale(d.Category); })
      .attr("width", xScale.bandwidth())
      .attr("y", function(d) { return yhist(d.Amount); })
	  .attr("fill", function(d, i) { return color(d.Color); } ) 
	  .attr("height", 0)
			.transition()
			.duration(200)
			.delay(function (d, i) {
				return i * 50;
			})
      .attr("height", function(d) { return h - yhist(d.Amount); });	 


  
	 
	 
  //Draw CDF line
  var guide = d3.line()
                .x(function(d) { return xScale(d.Category); })
                .y(function(d){ return ycum(d.CumulativePercentage) })
                .curve(d3.curveBasis);

  var line = svg.append('path')
                .datum(data)
                .attr('d', guide)
                .attr('class', 'line');


		
//Draw 80% line
  var guide2 = d3.line()
                .x(function(d) { return xScale(Horline); })
                .y(function(d){ return yhist(d.Amount) })
                .curve(d3.curveBasis);

  var line = svg.append('path')
                .datum(data)
                .attr('d', guide2)
                .attr('class', 'line');


var dotted=svg.selectAll(".dot")
    .data(dataset)
     .enter().append("circle") // Uses the enter().append() method
     .attr("class", "dot") // Assign a class for styling
     .attr("cx", function(d, i) { return xScale(Horline) })
     .attr("cy", function(d) { return ycum(Horper) })
      .attr("r", 5);				
	
dotted.append("svg:title") 
        .text(function(d) { return "80% Cumulative Point" ; })   	
				
  //Draw axes
  svg.append("g")
      .attr("class", "axisCSS")
      .attr("transform", "translate(0," + h + ")")
      .call(xAxis)
	  .selectAll("text")	
        .style("text-anchor", "end")
		 .attr("class","xlabels")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");


	//Draw y axis for cummulative percentage
    svg.append("g")
	      .attr("class", "axisCSS")
          .attr("transform", "translate(0, 0)")
          .call(yAxis2);	
    
 
    // Draw y axis label
    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - m.left)
      .attr("x",0 - (h / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Cummulative Percentage");
	

const tooltipLine = svg.append('line');

var  tipBox = svg.append('rect')
    .attr('width', w)
    .attr('height', h)
    .attr('opacity', 0)
    .on('mousemove', drawTooltip)
    .on('mouseout', removeTooltip);
	  
  function removeTooltip() {
    tooltip.style('display', 'none');
	tooltipLine.attr('stroke', 'none');
  }
  
    function drawTooltip() {
    var eachBand = xScale.step();
    var index = Math.floor((d3.mouse(tipBox.node())[0] / eachBand));
    var val = xScale.domain()[index];	 

    var amount=0;
	var cummulative=0;
	  
	data.forEach(function(d) {
      if(d.Category==val){
		 amount=d.Amount;
		 cummulative=d.CumulativePercentage;
	  }
     
  });


    tooltipLine.attr('stroke', 'black')
    .attr('x1', xScale(val)+eachBand/2)
    .attr('x2', xScale(val)+eachBand/2)
    .attr('y1', 0)
    .attr('y2', h);

  
    tooltip.style('left', (d3.event.pageX+10) + 'px')
    .style('top', (d3.event.pageY-10) + 'px')
    .style('display', 'inline-block')
	.html("Account: "+val+"<br>Potential Value: "+amount+"<br>Cummulative Percentage: "+cummulative);
  }

}	  