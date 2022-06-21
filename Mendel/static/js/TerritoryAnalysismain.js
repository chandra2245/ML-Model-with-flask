


queue()
	.defer(d3.json, piechartDataUrl_v2)
    .defer(d3.json, barchartDataUrl_v2)
	.defer(d3.json, paretochartDataUrl)
	.defer(d3.json, callslinechart)
	.defer(d3.json, callsstackchart)
    .defer(d3.json, decilebarchart)
    .await(ready);

function ready(error, dataset, datasetBarChart,datasetParetoChart,datasetcallslinechart,datacallsstackchart,datadecilebar) {
    d3PieChart_v2(dataset, datasetBarChart,'pieChart');
    d3BarChart_v2(datasetBarChart,'barChart','1',"Average Parameters");
	d3ParetoChart(datasetParetoChart,'paretoChart');
    d3CallsLineGraph(datasetcallslinechart,'CallsLine');
    d3CallsStackGraph(datacallsstackchart,"CallsStack",['High','Medium','Low','Non Target']);
    d3DecileBarChart(datadecilebar,"decileBar");
}