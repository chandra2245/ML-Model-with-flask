

function d3H2BarChartBase() {

    var margin = {top: 30, right: 5, bottom: 50, left: 50},
    width = 200 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom,
    colorBar = d3.scaleOrdinal(d3.schemeCategory10),
    barPadding = 1,
    misc = {ylabel: 7, xlabelH : 5, title:11};
    
    return {
        margin : margin, 
        width : width, 
        height : height, 
        colorBar : colorBar, 
        barPadding : barPadding,
        misc: misc
    };
}

function d3H2BarChart(datasetBarChart,chartID,svgid) {
	
	var basics = d3H2BarChartBase();
	
	var margin = basics.margin,
		width = basics.width,
	   height = basics.height,
		colorBar = basics.colorBar,
        barPadding = basics.barPadding,
        misc = basics.misc
		;
					
	var 	xScale = d3.scaleLinear()
						.domain([0, datasetBarChart.length])
						.range([0, width])
						;
						
	var yScale = d3.scaleLinear()
		   .domain([0, d3.max(datasetBarChart, function(d) { return d.measure; })])
           .range([height-36, 0]);
	
	var svg = d3.select(chartID)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("id","barChartPlot"+svgid)
    ;

    // Title

    svg.append("text")
    .attr("x", (width + margin.left + margin.right)/2)
    .attr("y", misc.title)
    .attr("class","title")				
    .attr("text-anchor", "middle")
    .text("Sales Attainment");

    var plot = svg
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + (margin.top + misc.ylabel) + ")");
            
    plot.selectAll("rect")
    .data(datasetBarChart)
    .enter()
    .append("rect")
        .attr("x", function(d, i) {
            return xScale(i);
        })
    .attr("width", width / datasetBarChart.length - barPadding)   
        .attr("y", function(d) {
            return yScale(d.measure);
        })  
	.attr("height", 0)
			.transition()
			.duration(200)
			.delay(function (d, i) {	
				return i * 50;
			})
    .attr("height", function(d) {
            return height-36-yScale(d.measure);
        })
    .attr("fill",function (d, i) {
				return colorBar[i];
			})
    
    	
	// Add y labels to plot	
	
	plot.selectAll("text")
	.data(datasetBarChart)
	.enter()
	.append("text")
	.text(function(d) {
			return d.measure;
	})
	.attr("text-anchor", "middle")

	.attr("x", function(d, i) {
			return (i * (width / datasetBarChart.length)) + ((width / datasetBarChart.length - barPadding) / 2);
	})
	.attr("y", function(d) {
			return (yScale(d.measure) - misc.ylabel);
	})
	.attr("class", "yAxis")
    ;
    
    // Add x labels to chart		
	var xcale = d3.scaleBand().rangeRound([50, width+50]).padding(0.1);
    xcale.domain(datasetBarChart.map(function(d) { return d.category; }));
  
	var xAxis = d3.axisBottom(xcale);

	
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
	  .selectAll("text")	
        .style("text-anchor", "end")
		.attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)"); 				
}