var formatAsInteger = d3.format(",");

function d3PieChart_v2(dataset, datasetBarChart, chartID){

    var margin = {top: 50, right: 5, bottom: 20, left: 50};
     
    var   piediv=d3.select("#"+chartID);
    
    var width = parseInt(piediv.style("width")) - margin.left - margin.right ,
        height = 400 - margin.top - margin.bottom,
        outerRadius = Math.min(width, height) / 2,
        innerRadius = outerRadius * .999,   
        innerRadiusFinal = outerRadius * .5,
        innerRadiusFinal3 = outerRadius* .45,
        color = d3.scaleOrdinal(d3.schemeCategory10);   
    
    var vis = d3.select("#"+chartID)
	    .append("svg")  
	    .data([dataset])    
	    .attr("width", width)
	    .attr("height", height)
	    .append("svg:g")   
	    .attr("transform", "translate(" + outerRadius + "," + outerRadius + ")"); 
		
	let tooltip = d3.select('body').append('div')
                  .attr('class', 'tooltips')
                  .attr('id',"tooltip"+chartID);
				  
	let bartooltip = d3.select('body').append('div')
                  .attr('class', 'bartooltip')
                  .attr('id',"barChart");
    
   function showTooltip(d) {
	   bartooltip.style('left', (d3.event.pageX+10) + 'px')
       .style('top', (d3.event.pageY-10) + 'px')
       .style('display', 'inline-block');
    }

  function hideTooltip() {
	bartooltip.style('display', 'none');
  }
	
	
    var arc = d3.arc()    
        .outerRadius(outerRadius).innerRadius(0);

    var arcFinal = d3.arc().innerRadius(innerRadiusFinal).outerRadius(outerRadius);
    var arcFinal3 = d3.arc().innerRadius(innerRadiusFinal3).outerRadius(outerRadius);   

    var pie = d3.pie() 
        .value(function(d) { return d.measure; }); 
    
    var arcs = vis.selectAll("g.slice")
        .data(pie)                     
        .enter()                       
        .append("svg:g")               
        .attr("class", "slice") 
        .on("mouseover", mouseover)
    	.on("mouseout", mouseout)
    	.on("click", up);
    				
    arcs.append("svg:path")
        .attr("fill", function(d, i) { return color(i); } ) 
        .attr("d", arc)     
			

    d3.selectAll("g.slice").selectAll("path").transition()
		.duration(750)
		.delay(10)
        .attr("d", arcFinal );
    
    
    arcs.filter(function(d) { return d.endAngle - d.startAngle > .2; })
    .append("svg:text")
    .attr("dy", ".35em")
    .attr("text-anchor", "middle")
    .attr("transform", function(d) { return "translate(" + arcFinal.centroid(d) + ")"; })
    .text(function(d) { return d.data.category; });

 //   vis.append("svg:text")
   //     .attr("dy", ".35em")
     //   .attr("text-anchor", "middle")
    //    .text("Clusters")
    //    .attr("class","title");		    

    function mouseover(d) {
        d3.select(this).select("path").transition()
        .duration(750)
        .attr("d", arcFinal3);
		showTooltip(d);
		up(d);
    }

    function mouseout() {
        d3.select(this).select("path").transition()
        .duration(750)
        .attr("d", arcFinal);
		hideTooltip();
    }

    function up(d, i) {
        
        updateBarChart_v2(d.data.category, color(i), datasetBarChart);

     }
}

