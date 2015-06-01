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
place[2] = new pn.Place({ position: { x: 350, y: 160 }, attrs: { '.label': { text: 'p3' } }, name: 'p3', tokens: 12 });
place[3] = new pn.Place({ position: { x: 550, y: 50 }, attrs: { '.label': { text: 'p4' } }, name: 'p4', tokens: 1 });
place[4] = new pn.Place({ position: { x: 560, y: 260 }, attrs: { '.label': { text: 'p5' } }, name: 'p5', tokens: 3 });

//transitions
var trans = [];

trans[0] = new pn.Transition({ position: { x: 50, y: 160 }, attrs: { '.label': { text: 't1' } }, name: 't1', priority: 1 });
trans[1] = new pn.Transition({ position: { x: 270, y: 160 }, attrs: { '.label': { text: 't2' } }, name: 't2', priority: 1 });
trans[2] = new pn.Transition({ position: { x: 470, y: 160 }, attrs: { '.label': { text: 't3' } }, name: 't3', priority: 1 });
trans[3] = new pn.Transition({ position: { x: 680, y: 160 }, attrs: { '.label': { text: 't4' } }, name: 't4', priority: 1 });

//links
var link = [];

link[0] = new pn.Link({ source: { id: trans[0].id, selector: '.root' }, target: { id: place[0].id, selector: '.root' }, direction: 1 ,weight: 1 });
link[1] = new pn.Link({ source: { id: place[0].id, selector: '.root' }, target: { id: trans[1].id, selector: '.root' }, direction: 0 ,weight: 1 });
link[2] = new pn.Link({ source: { id: trans[1].id, selector: '.root' }, target: { id: place[1].id, selector: '.root' }, direction: 1 ,weight: 1 });
link[3] = new pn.Link({ source: { id: place[1].id, selector: '.root' }, target: { id: trans[0].id, selector: '.root' }, direction: 0, weight: 1 });
link[4] = new pn.Link({ source: { id: trans[1].id, selector: '.root' }, target: { id: place[2].id, selector: '.root' }, direction: 1, weight: 1 });
link[5] = new pn.Link({ source: { id: place[2].id, selector: '.root' }, target: { id: trans[2].id, selector: '.root' }, direction: 0, weight: 1 });
link[6] = new pn.Link({ source: { id: trans[2].id, selector: '.root' }, target: { id: place[3].id, selector: '.root' }, direction: 1, weight: 1 });
link[7] = new pn.Link({ source: { id: place[3].id, selector: '.root' }, target: { id: trans[3].id, selector: '.root' }, direction: 0, weight: 1 });
link[8] = new pn.Link({ source: { id: trans[3].id, selector: '.root' }, target: { id: place[4].id, selector: '.root' }, direction: 1, weight: 1 });
link[9] = new pn.Link({ source: { id: place[4].id, selector: '.root' }, target: { id: trans[2].id, selector: '.root' }, direction: 0, weight: 1 });

//build graph
graph.addCell([
	place[0],
	place[1],
	place[2],
	place[3],
	place[4],
	trans[0],
	trans[1],
	trans[2],
	trans[3],
	link[0],
	link[1],
	link[2],
	link[3],
	link[4],
	link[5],
	link[6],
	link[7],
	link[8],
	link[9]
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
		place[place.length] = new pn.Place({ position: { x: xPos - 32, y: yPos - 32 }, attrs: { '.label': { text: label } }, tokens: parseInt(tokens) })
		]);
	}

function addTrans(xPos, yPos, label, priority) {
	graph.addCell([
		trans[trans.length] = new pn.Transition({ position: { x: xPos - 13, y: yPos - 32 }, attrs: { '.label': { text: label } }, priority: parseInt(priority) })
		]);
	}

//add mode
$('#add-place').change(function() {
	$('label[for="add-content"]').html('Tokens');
	});

$('#add-trans').change(function() {
	$('label[for="add-content"]').html('Priority');
	});

//validate node
function validateNode() {
	if($('#add-label').val().trim() && getNodeByLabel($('#add-label').val()) == null && $('#add-content').val().trim() && Number.isInteger(parseInt($('#add-content').val()))) {
		$('#add-info').html('Double click on paper to add');
		return true;
		}
	else {
		$('#add-info').html('Fill in inputs with correct values to add');
		return false;
		}
	}

$('#add-label, #add-content').change(validateNode);

$('#paper').dblclick(function() {
	if(validateNode()) {
		if($('#add-place').is(':checked'))
			addPlace(cursorPos.x, cursorPos.y, $('#add-label').val(), $('#add-content').val());
		else
			addTrans(cursorPos.x, cursorPos.y, $('#add-label').val(), $('#add-content').val());
		$('#add-label, #add-content').val('');
		validateNode();
		updatePanel();
		}
	else {
		console.log('ERROR');
		}
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
	if(getNodeById(id).prop('type') == 'pn.Place')
		place.splice(getNodeIndex(id), 1);
	else
		trans.splice(getNodeIndex(id), 1);
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

//validate link
function validateLink(nodes) {
var falg = true, array;
link.forEach(function(e) {
		array = [e.prop('source').id, e.prop('target').id];
		if(!($(nodes).not(array).length && $(array).not(nodes).length))
			flag = false;
	});
return flag;
}

//add link
function addLink(nodes, direction, weight) {
	
	console.log(validateLink(nodes));

	$('#add-label, #add-content').val('');
	if(direction)
		nodes.reverse();
	graph.addCell([
		link[link.length] = new pn.Link({ source: { id: nodes[0], selector: '.root' }, target: { id: nodes[1], selector: '.root' }, direction: direction, weight: weight })
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

	//!disable/eanble btns
	}
	
//fire transition
function fireTransition(trans, sec) {
	var inbound = graph.getConnectedLinks(trans, { inbound: true });
	var outbound = graph.getConnectedLinks(trans, { outbound: true });
	
	var placesBefore = _.map(inbound, function (link) { return graph.getCell(link.get('source').id); });
	var placesAfter = _.map(outbound, function (link) { return graph.getCell(link.get('target').id); });
	
	_.each(placesBefore, function (p) {
		var link = _.find(inbound, function (l) { return l.get('source').id === p.id; });
		paper.findViewByModel(link).sendToken(V('circle', { r: 5, fill: 'red' }).node, sec * 1000);
		});
	
	_.each(placesAfter, function (p) {
		var link = _.find(outbound, function (l) { return l.get('target').id === p.id; });
		paper.findViewByModel(link).sendToken(V('circle', { r: 5, fill: 'red' }).node, sec * 1000);
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
		var links_in_ids = [], links_out_ids = [];
		link.forEach(function(ie, ii) {
			if(oe.id == ie.prop('source').id || oe.id == ie.prop('target').id)
				if(ie.prop('direction'))
					links_out_ids.push(ii);
				else
					links_in_ids.push(ii);
			});
		transitions += '{"id":'+ oi +',"name":"'+ oe.attr('.label').text +'","priority":'+ oe.prop('priority') +',"links_in_ids":'+ JSON.stringify(links_in_ids) +',"links_out_ids":'+ JSON.stringify(links_out_ids) +'},';
		});
	transitions = transitions.slice(0,-1) + ']';

	var links = '"links": [';
	link.forEach(function(e, i) {
		links += '{"id":'+ i +',"place_id":'+ (e.prop('direction') ? getNodeIndex(e.prop('target').id) : getNodeIndex(e.prop('source').id)) +',"direction":'+ e.prop('direction') +',"weight":'+ e.prop('weight') +'},';
		});
	links = links.slice(0,-1) + ']';

	return '"data":{'+ links +','+ places +','+ transitions +'}';
	}

//deserialize graph
function deserializeGraph(data) {
	fireTransition(trans[data.id], 1);
	data.links_in.concat(data.links_out).forEach(function(e) {
		e = e.place;
		place[e.id].prop('tokens', e.tokens);
		});
	}

//web socket connection
socket = new WebSocket("ws://localhost:8888/websocket");

//response handler
socket.onmessage = function(e) {
	var data = JSON.parse(e.data);
	switch(data.type) {
		case 2:
			deserializeGraph(data.data);
		break;
		default:
			console.log('ERROR');
		}
	console.log(e.data);
	};

//simulation
var simulation;

//send graph
function sendGraph() {
	socket.send('{"type":1,'+ serializeGraph() +'}');
	}

//simulation step
function simulationStep() {
	socket.send('{"type":2}');
	}

//start simulation
function startSimulation() {
	sendGraph();
	simulation = setInterval(simulationStep(), 1000);
	}
	
//stop simulation
function stopSimulation() {
	clearInterval(simulation);
	}

//get parameters
function getParameters() {
	socket.send('{"type":3}');
	}

//onload
$(function() {
	updatePanel();
	});