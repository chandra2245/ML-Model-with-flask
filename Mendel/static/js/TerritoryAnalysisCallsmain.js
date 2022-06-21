

queue()
	.defer(d3.json, decileData)
    .await(ready);

function ready(error, datasetdecileChart) {
   if(DecileFilter=='Brand Category'){
    d3CallsStackGraph(datasetdecileChart,"CallsStack",['PLANNED','UNPLANNED']);
}
   if(DecileFilter=='Decile'){
    d3CallsStackGraph(datasetdecileChart,"CallsStack",['High','Medium','Low','Non Target']);
}
   if(DecileFilter=='Call Category'){
    d3CallsStackGraph(datasetdecileChart,"CallsStack",['HCI/HCO Call','HCP Detail Call','HCP Sample Call','Pharmacy Call','HCP Detail Call Prescriber']);

}
}