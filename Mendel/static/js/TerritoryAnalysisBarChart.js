var group = "All";
    
function datasetBarChosen_v2(group, datasetBarChart) {
        var ds = [];
        for (x in datasetBarChart) {
             if(datasetBarChart[x].group==group){
                 ds.push(datasetBarChart[x]);
             } 
            }
        return ds;
}

function d3BarChartBase_v2() {

    var margin = {top: 30, right: 5, bottom: 70, left: 50},
    width = 400 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom,
    colorBar = d3.scaleOrdinal(d3.schemeCategory10),
    barPadding = 1,
    misc = {ylabel: 7, xlabelH : 5, title:15};
    
    return {
        margin : margin, 
        width : width, 
        height : height, 
        colorBar : colorBar, 
        barPadding : barPadding,
        misc: misc
    };
}

function d3BarChart_v2(datasetBarChart,chartID,svgid,barheader) {
	var firstDatasetBarChart = datasetBarChosen_v2(group, datasetBarChart);         	
	
	var basics = d3BarChartBase_v2();
	
	var margin = basics.margin,
		width = basics.width,
	   height = basics.height,
		colorBar = basics.colorBar,
        barPadding = basics.barPadding,
        misc = basics.misc
		;
					
	var 	xScale = d3.scaleLinear()
						.domain([0, firstDatasetBarChart.length])
						.range([0, width])
						;
						
	var yScale = d3.scaleLinear()
		   .domain([0, 5])
           .range([height-36, 0]);
	
	var yAxis = d3.axisLeft(yScale);
	
	var svg = d3.select("#"+chartID)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("id","barChart_v2Plot"+svgid)
    ;

   let tooltip = d3.select('body').append('div')
      .attr('class', 'tooltips')
      .attr('id',"tooltip"+chartID);
    
   function showTooltip(d) {
       tooltip.style('left', (d3.event.pageX+10) + 'px')
       .style('top', (d3.event.pageY-10) + 'px')
       .style('display', 'inline-block')
       .html(d.category+": "+d.value);
    }

  function hideTooltip() {
    tooltip.style('display', 'none');
  }
	

   // Title

    svg.append("text")
    .attr("x", (width + margin.left + margin.right)/2)
    .attr("y", misc.title)
    .attr("class","title")				
    .attr("text-anchor", "middle")
    .text("Scaled Parameters of Accounts");

    var plot = svg
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + (margin.top + misc.ylabel) + ")");
            
    var bar=plot.selectAll(".bar")
    .data(firstDatasetBarChart)
    .enter()
    .append("g")
    .attr("class", "bar");

    

    bar.append("rect")
        .attr("x", function(d, i) {
            return xScale(i);
        })
    .attr("width", width / firstDatasetBarChart.length - barPadding)   
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
    .attr("fill", "#3cb371");
    
    	
       bar.on("mouseover", showTooltip);
       bar.on("mouseout", hideTooltip);
        

	// Add y labels to plot	
	
	plot.selectAll("text")
	.data(firstDatasetBarChart)
	.enter()
	.append("text")
	.text(function(d) {
			return formatAsInteger(d.measure);
	})
	.attr("text-anchor", "middle")

	.attr("x", function(d, i) {
			return (i * (width / firstDatasetBarChart.length)) + ((width / firstDatasetBarChart.length - barPadding) / 2);
	})
	.attr("y", function(d) {
			return (yScale(d.measure) - misc.ylabel);
	})
	.attr("class", "yAxis")
    ;
    
    // Add x labels to chart		
	var xcale = d3.scaleBand().rangeRound([50, width+50]).padding(0.1);
    xcale.domain(firstDatasetBarChart.map(function(d) { return d.category; }));
  
	var xAxis = d3.axisBottom(xcale);

	
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
	  .selectAll("text")	
        .style("text-anchor", "end")
		.attr("class","xlabels")
		.attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-40)"); 		

  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate("+ margin.left +","+(margin.top+6)+")")
      .call(yAxis)
	  .selectAll("text")	
        .style("text-anchor", "end")
		.attr("class","xlabels")
      .attr("dy", ".71em")
      .style("text-anchor", "end");
		
}