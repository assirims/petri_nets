//graph
var graph = new joint.dia.Graph;

//paper
var paper = new joint.dia.Paper({
	el: $('#paper'),
	width: 1000,
	height: 500,
	gridSize: 10,
	perpendicularLinks: true,
	model: graph
	});

var pn = joint.shapes.pn;

//places
var place = [];

place[0] = new pn.Place({ position: { x: 140, y: 50 }, attrs: { '.label': { text: 'p1' } }, name: 'p1', tokens: 1 });
place[1] = new pn.Place({ position: { x: 140, y: 260 }, attrs: { '.label': { text: 'p2' } }, name: 'p2', tokens: 2 });

//transitions
var trans = [];

trans[0] = new pn.Transition({ position: { x: 50, y: 160 }, attrs: { '.label': { text: 't1' } }, name: 't1', priority: 4 });

//links
var link = [];

link[0] = new pn.Link({ source: { id: place[0].id, selector: '.root' }, target: { id: trans[0].id, selector: '.root' }, direction: 0 ,weight: 1 });
link[1] = new pn.Link({ source: { id: trans[0].id, selector: '.root' }, target: { id: place[1].id, selector: '.root' }, direction: 1 ,weight: 1 });

//build graph
graph.addCell([
	place[0],
	place[1],
	trans[0],
	link[0],
	link[1]
	]);

//cursor position
var cursorPos = {};

$('#paper').mousemove(function(e){
	cursorPos = {
		x: e.pageX,
		y: e.pageY
		};
	});

//add node
function addPlace(xPos, yPos, label, tokens) {
	graph.addCell([
		place[place.length] = new pn.Place({ position: { x: xPos - 32, y: yPos - 32 }, attrs: { '.label': { text: label } }, tokens: tokens })
		]);
	}

function addTrans(xPos, yPos, label, priority) {
	graph.addCell([
		trans[trans.length] = new pn.Transition({ position: { x: xPos - 13, y: yPos - 32 }, attrs: { '.label': { text: label } }, priority: priority })
		]);
	}

//add mode
$('#add-place').change(function() {
	$('label[for="add-content"]').html('Tokens');
	});

$('#add-trans').change(function() {
	$('label[for="add-content"]').html('Priority');
	});

$('#paper').dblclick(function() {
	//!validate
	//console.log($('#add-label').val() && getNodeByLabel($('#add-label').val())==null && $('#add-tokens').val());
	//updatePanel();
	if($('#add-place').attr('checked'))
		addPlace(cursorPos.x, cursorPos.y, $('#add-label').val(), $('#add-content').val());
	else
		addTrans(cursorPos.x, cursorPos.y, $('#add-label').val(), $('#add-content').val());
	});

//get node
function getNodeById(id) {
	var node = null;
	place.concat(trans).forEach(function(e) {
		if(e.id == id)
			node = e;
		});
	return node;
	}

function getNodeByLabel(label) {
	var node = null;
	place.concat(trans).forEach(function(e) {
		if(e.attr('.label').text == label)
			node = e;
		});
	return node;
	}

//get node index
function getNodeIndex(id) {
	var index;
	[place.indexOf(getNodeById(id)), trans.indexOf(getNodeById(id))].forEach(function(e) {
		if(e != -1)
			index = e;
		});
		return index;
	}

//delete node
function deleteNode(id) {
	getNodeById(id).remove();

	array.splice(index, array.indexOf(5));

	updatePanel();
	}

$('#delete').click(function() {
	deleteNode($('#delete-list').val());
	});

//link direction
$('#link-direction').click(function() {
		if($(this).data('direction'))
			$(this).removeClass('glyphicon glyphicon-arrow-left').addClass('glyphicon glyphicon-arrow-right');
		else
			$(this).removeClass('glyphicon glyphicon-arrow-right').addClass('glyphicon glyphicon-arrow-left');
		$(this).data('direction',+!$(this).data('direction'));
		});

//add link
function addLink(nodes, direction, weight) {
	//!validate empty/duplicate
	if(direction)
		nodes.reverse();
	graph.addCell([
		link[link.length] = new pn.Link({ source: { id: getNodeById(nodes[0]).id, selector: '.root' }, target: { id: getNodeById(nodes[1]).id, selector: '.root' }, direction: direction, weight: weight })
		]);
	}

$('#link').click(function() {
	addLink([$('#link-place').val(), $('#link-trans').val()], $('#link-direction').data('direction'), $('#link-weight').val())
	});

//update panel
function updatePanel() {
	$('#link-place, #link-trans, #delete-list optgroup[label=Places], #delete-list optgroup[label=Transitions]').empty();

	place.forEach(function(e) {
		$('#link-place, #delete-list optgroup[label=Places]').append($('<option>', {value: e.id, text: e.attr('.label').text}));
		});

	trans.forEach(function(e) {
		$('#link-trans, #delete-list optgroup[label=Transitions]').append($('<option>', {value: e.id, text: e.attr('.label').text}));
		});
	}

//serialize graph
function serializeGraph() {

	var places = '"places": [';
	place.forEach(function(e, i) {
		places += '{"id":'+ i +',"name":"'+ e.attr('.label').text +'","tokens":'+ e.prop('tokens') +'},';
		});
	places = places.slice(0,-1) + ']';

	var transitions = '"transitions": [';
	trans.forEach(function(oe, oi) {
		var connectors_in_ids = [], connectors_out_ids = [];
		link.forEach(function(ie, ii) {
			if(oe.id == ie.prop('source').id || oe.id == ie.prop('target').id)
				if(ie.prop('direction'))
					connectors_out_ids.push(ii);
				else
					connectors_in_ids.push(ii);
			});
		transitions += '{"id":'+ oi +',"name":"'+ oe.attr('.label').text +'","priority":'+ oe.prop('priority') +',"links_in_ids":'+ JSON.stringify(connectors_in_ids) +',"links_out_ids":'+ JSON.stringify(connectors_out_ids) +'},';
		});
	transitions = transitions.slice(0,-1) + ']';

	var connectors = '"links": [';
	link.forEach(function(e, i) {
		connectors += '{"id":'+ i +',"place_id":'+ getNodeIndex(e.prop('source').id) +',"direction":'+ e.prop('direction') +',"weight":'+ e.prop('weight') +'},';
		});
	connectors = connectors.slice(0,-1) + ']';

	return '"data":{'+ connectors +','+ places +','+ transitions +'}';
	}

//deserialize graph
function deserializeGraph(graph) {
	graph.data.places.forEach(function(e, i) {
		place[i].prop('tokens', e.tokens);
		});
	}

//onload
$(function() {
	updatePanel();
	});


//------------------------TESTS---------------------------------

ws = new WebSocket("ws://localhost:8888/websocket");
ws.onmessage = function(e) {

    //var data = JSON.parse(e.data);

    //if (data.type == 2) {
    //    deserializeGraph(data);
    //}
    console.log(e.data);
};

function send() {

    console.log('{"type":1,'+ serializeGraph() +'}')
	ws.send('{"type":1,'+ serializeGraph() +'}');
	}

function send2(type) {
	ws.send('{"type": 2, "data": ""}');
	}

/*
attrs: { '.label': { Objectfill: "#000000", font-size: 12, text: "qweety", ref: "rect",ref-x: 0.5,ref-y: -20,text-anchor: "middle" } }
ref-x: 0.5ref-y: -20text: "t1"text-anchor: "middle"

function fireTransition(t, sec) {

	var inbound = graph.getConnectedLinks(t, { inbound: true });
	var outbound = graph.getConnectedLinks(t, { outbound: true });

	var placesBefore = _.map(inbound, function (link) { return graph.getCell(link.get('source').id); });
	var placesAfter = _.map(outbound, function (link) { return graph.getCell(link.get('target').id); });

	var isFirable = true;
	_.each(placesBefore, function (p) { if (p.get('tokens') == 0) isFirable = false; });

	if (isFirable) {

		_.each(placesBefore, function (p) {
			// Let the execution finish before adjusting the value of tokens. So that we can loop over all transitions
			// and call fireTransition() on the original number of tokens.
			_.defer(function () { p.set('tokens', p.get('tokens') - 1); });
			var link = _.find(inbound, function (l) { return l.get('source').id === p.id; });
			paper.findViewByModel(link).sendToken(V('circle', { r: 5, fill: 'red' }).node, sec * 1000);
			});

		_.each(placesAfter, function (p) {
			var link = _.find(outbound, function (l) { return l.get('target').id === p.id; });
			paper.findViewByModel(link).sendToken(V('circle', { r: 5, fill: 'red' }).node, sec * 1000, function () {
				p.set('tokens', p.get('tokens') + 1);
				});

			});
		}
	}

function simulate() {
	var transitions = [trans[0], trans[1], trans[2], trans[3]];
	_.each(transitions, function (t) { if (Math.random() < 0.7) fireTransition(t, 1); });

	return setInterval(function () {
		_.each(transitions, function (t) { if (Math.random() < 0.7) fireTransition(t, 1); });}, 2000);
	}

function stopSimulation(simulationId) {
	clearInterval(simulationId);
	}

var simulationId = simulate();
*/