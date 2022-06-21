function scatterplotChart(divid, data) { 

    var   scatterdiv=d3.select(divid);


    var margin = {top: 20, right: 20, bottom: 40, left: 60},
        width = parseInt(scatterdiv.style("width")) - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;
    
    var x = d3.scaleLinear()
        .range([0, width]);
    
    var y = d3.scaleLinear()
        .range([height, 0]);
    
    var color = d3.scaleOrdinal(d3.schemeCategory10);
    
    var xAxis = d3.axisBottom(x);
    
    var yAxis = d3.axisLeft(y);
	
	var symbols = d3.scaleOrdinal(d3.symbols);

    // creates a generator for symbols
    var symbol = d3.symbol().size(80);  
    
var svg = d3.select(divid).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
	let tooltip = d3.select('body').append('div')
                  .attr('class', 'tooltips')
                  .attr('id',"tooltip"+divid);	
    
   function showTooltip(d) {
       tooltip.style('left', (d3.event.pageX+10) + 'px')
       .style('top', (d3.event.pageY-10) + 'px')
       .style('display', 'inline-block')
	  .html("Name: "+d.name+"<br>Probability Score: "+d.Probability_Score+"<br>Potential Value: "+d.Potential_Value);
    }

  function hideTooltip() {
    tooltip.style('display', 'none');
  }
	
    
      x.domain(d3.extent(data, function(d){
		return d.Probability_Score;
	   })).nice();
      
	  y.domain(d3.extent(data, function(d){
		return d.Potential_Value;
	   })).nice();

    
      svg.append("g")
          .attr("class", "axisCSS")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
        .append("text")
          .attr("class", "label")
          .attr("x", width)
          .attr("y", -6)
          .style("text-anchor", "end");
    
      svg.append("g")
          .attr("class", "axisCSS")
          .call(yAxis)
        .append("text")
          .attr("class", "label")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end");
    
      svg.selectAll(".symbol")
          .data(data)
          .enter().append("path")
          .attr("class", "symbol")
          .attr("d", function(d, i) { return symbol.type(symbols(d.Segment))(); })
          .style("fill", function(d) { return color(d.Segment); })
          .attr("transform", function(d) { 
                  return "translate(" + x(d.Probability_Score) + "," + y(d.Potential_Value) +")"; 
                })
          .on("mouseover", mouseover)
    	  .on("mouseout", mouseout);
    
    function mouseover(d) {
        d3.select(this).select("path").transition()
        .duration(750)
        .attr("r", 10);
		showTooltip(d);
    }

    function mouseout() {
        d3.select(this).select("path").transition()
        .duration(750)
        .attr("r", 4.5);
		hideTooltip();
    }

var clicked = ""
  
  var legend = svg.selectAll(".legend")
    .data(color.domain())
  .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("path")
    .style("fill", function(d) { return color(d); })
    	.attr("d", function(d, i) { return symbol.type(symbols(d))(); })
	    .attr("transform", function(d, i) { 
    		return "translate(" + (width -10) + "," + 10 + ")";
  		})
  		.on("click",function(d){
              d3.selectAll(".symbol").style("opacity",1)
   
               if (clicked !== d){
                 d3.selectAll(".symbol")
                   .filter(function(e){
                   return e.Segment !== d;
                 })
                   .style("opacity",0.1)
                 clicked = d
               }
                else{
                  clicked = ""
                }
          });
		  
		  
      legend.append("text")
          .attr("x", width - 24)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) { return d; });



  // text label for the x axis
  svg.append("text")             
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top+margin.bottom-25) + ")")
      .style("text-anchor", "middle")
      .text("Propensity Score");

  // text label for the y axis
  svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Total Potential Value");      


    
}