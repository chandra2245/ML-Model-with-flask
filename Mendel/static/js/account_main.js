


queue()
	.defer(d3.json, hbarchartDataUrl)
	.defer(d3.json, linechartDataUrl)
	.defer(d3.json, gaugechartDataUrl)
   .await(ready);

function ready(error, dataset,timedata,gaugedata) {
    d3RadialBarGraph(dataset,'#hbarChart','1','Sales','Sales Analysis');
	d3RadialBarGraph(dataset,'#hbarChart2','2','Comp_Analysis','Competitor Analysis');
	d3LineGraph(timedata,'#LineChart');
	loadLiquidFillGauge('#gaugeChart',gaugedata);
}