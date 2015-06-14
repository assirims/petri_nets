//window dimensions
var windowDim = {};
windowDim = {
		width: $(document).width() - 5,
		height: $(document).height() - 5
		};

//cursor position
var cursorPos = {};

$('#paper').mousemove(function(e){
	cursorPos = {
		x: e.pageX,
		y: e.pageY
		};
	});

//petri network
var petrinet = new joint.dia.Graph;

//paper
var paper = new joint.dia.Paper({ el: $('#paper'), width: windowDim.width - 250, height: windowDim.height, gridSize: 10, perpendicularLinks: true, model: petrinet });

var pn = joint.shapes.pn;

//create model places
petrinet.addCell([
	new pn.Place({ position: { x: 240, y: 150 }, attrs: { '.label': { text: 'p1' } }, name: 'p1', tokens: 1 }),
	new pn.Place({ position: { x: 240, y: 360 }, attrs: { '.label': { text: 'p2' } }, name: 'p2', tokens: 2 })
	]);

//create model transitions
petrinet.addCell([
	new pn.Transition({ position: { x: 150, y: 260 }, attrs: { '.label': { text: 't1 [1]' } }, name: 't1', priority: 1 }),
	new pn.Transition({ position: { x: 370, y: 260 }, attrs: { '.label': { text: 't2 [1]' } }, name: 't2', priority: 1 })
	]);
	
//create model links
petrinet.addCell([
	new pn.Link({ source: { id: transArray()[0].id, selector: '.root' }, target: { id: placeArray()[0].id, selector: '.root' }, labels: [{ position: .5, attrs: { text: { text: 1 } } }], direction: 1 ,weight: 1 }),
	new pn.Link({ source: { id: placeArray()[0].id, selector: '.root' }, target: { id: transArray()[1].id, selector: '.root' }, labels: [{ position: .5, attrs: { text: { text: 1 } } }], direction: 0 ,weight: 1 }),
	new pn.Link({ source: { id: transArray()[1].id, selector: '.root' }, target: { id: placeArray()[1].id, selector: '.root' }, labels: [{ position: .5, attrs: { text: { text: 1 } } }], direction: 1 ,weight: 1 }),
	new pn.Link({ source: { id: placeArray()[1].id, selector: '.root' }, target: { id: transArray()[0].id, selector: '.root' }, labels: [{ position: .5, attrs: { text: { text: 1 } } }], direction: 0, weight: 1 })
	]);

//add place
function addPlace(xPos, yPos, label, tokens) {
	petrinet.addCell(new pn.Place({ position: { x: xPos - 32, y: yPos - 32 }, attrs: { '.label': { text: label } }, name: label, tokens: parseInt(tokens) }));
	}

//add transitions
function addTrans(xPos, yPos, label, priority) {
	petrinet.addCell(new pn.Transition({ position: { x: xPos - 13, y: yPos - 32 }, attrs: { '.label': { text: label + ' [' + priority + ']' } }, name: label, priority: parseInt(priority) }));
	}
	
//add cell mode
$('#add-place').change(function() {
	$('label[for="add-content"]').html('Tokens');
	});

$('#add-trans').change(function() {
	$('label[for="add-content"]').html('Priority');
	});
	
//validate node
function validateNode() {
	if($('#add-label').val().trim() && getByName($('#add-label').val()) == null && $('#add-content').val().trim() && Number.isInteger(parseInt($('#add-content').val())))
		return true;
	else
		return false;
	}

$('#paper').dblclick(function() {
	if(validateNode()) {
		if($('#add-place').is(':checked'))
			addPlace(cursorPos.x, cursorPos.y, $('#add-label').val(), $('#add-content').val());
		else
			addTrans(cursorPos.x, cursorPos.y, $('#add-label').val(), $('#add-content').val());
		$('#add-label, #add-content').val('');
		updatePanel();
		}
	else {
		console.log('ERROR: Invalid node data');
		alertMsg('Invalid node data');
		}
	});
	
//get array index
function getIndex(id) {
	var index;
	[placeArray().indexOf(petrinet.getCell(id)), transArray().indexOf(petrinet.getCell(id))].forEach(function(e) {
		if(e != -1)
			index = e;
		});
		return index;
	}
	
//get cell by name
function getByName(name) {
	var cell = null;
	placeArray().concat(transArray()).forEach(function(e) {
		if(e.prop('name') == name)
			cell = e;
		});
	return cell;
	}

//check place
function isPlace(cell) {
	if(cell.prop('type') == 'pn.Place')
		return true;
	return false;
	}
	
//check transition
function isTrans(cell) {
	if(cell.prop('type') == 'pn.Transition')
		return true;
	return false;
	}

//get places array
function placeArray() {
	var array = [];
	petrinet.getElements().forEach(function(e) {
		if(isPlace(e))
			array.push(e);
		});
	return array;
	}

//get transitions array	
function transArray() {
	var array = [];
	petrinet.getElements().forEach(function(e) {
		if(isTrans(e))
			array.push(e);
		});
	return array;
	}
	
//get links array
function linkArray() {
	return petrinet.getLinks();
	}

//delete cell
$('#paper').delegate('.pn', 'mousedown', function(e) {
	if(e.which == 2) {
		petrinet.getCell($(this).attr('model-id')).remove();
		updatePanel();
		}
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
function validateLink(cells) {
	var flag = true, array;
	linkArray().forEach(function(e) {
		array = [e.prop('source').id, e.prop('target').id];
		if(!($(cells).not(array).length && $(array).not(cells).length) || !Number.isInteger(parseInt($('#link-weight').val())))
			flag = false;
		});
	return flag;
	}

//add link
function addLink(nodes, direction, weight) {
	if(validateLink(nodes)) {
		$('#add-label, #add-content').val('');
		if(direction)
			nodes.reverse();
		petrinet.addCell(new pn.Link({ source: { id: nodes[0], selector: '.root' }, target: { id: nodes[1], selector: '.root' }, labels: [{ position: .5, attrs: { text: { text: parseInt(weight) } } }], direction: direction, weight: parseInt(weight) }));
		}
	else {
		console.log('ERROR: Invalid link data or duplicate');
		alertMsg('Invalid link data or duplicate');
		}
	}

$('#link').click(function() {
	addLink([$('#link-place').val(), $('#link-trans').val()], $('#link-direction').data('direction'), $('#link-weight').val())
	});

//open simulation mode
$('#simulation').click(function() {
	$('#build-tab').hide();
	$('#simulation-tab').show();
	sendGraph();
	});

//open build mode
$('#build').click(function() {
	$('#simulation-tab').hide();
	$('#build-tab').show();
	});

//alert message
function alertMsg(msg) {
	$('.info').html(msg);
	$('.info').fadeIn('slow');
	setTimeout(function() { $('.info').fadeOut('slow'); }, 4000);
	}

//update panel
function updatePanel() {
	
	$('#link-place > optgroup, #link-trans > optgroup').empty();
	
	placeArray().forEach(function(e) {
		$('#link-place > optgroup').append($('<option>', { value: e.id, text: e.attr('.label').text }));
		});
		
	transArray().forEach(function(e) {
		$('#link-trans > optgroup').append($('<option>', { value: e.id, text: e.attr('.label').text }));
		});
	
	if(!($('#link-place:has(option)').length && $('#link-trans:has(option)').length))
		$('#link').attr('disabled', true);
	else
		$('#link').attr('disabled', false);
	}

//update link arrows
function updateLinks() {
	petrinet.getLinks().forEach(function(e) {
		e.attr({ '.marker-target': { d: 'M 10 0 L 0 5 L 10 10 z' } });
		});
	}

//fire transition
function fireTransition(trans, sec) {
	var inbound = petrinet.getConnectedLinks(trans, { inbound: true });
	var outbound = petrinet.getConnectedLinks(trans, { outbound: true });
	
	var placesBefore = _.map(inbound, function (link) { return petrinet.getCell(link.get('source').id); });
	var placesAfter = _.map(outbound, function (link) { return petrinet.getCell(link.get('target').id); });
	
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
	placeArray().forEach(function(e, i) {
		places += '{ "id": '+ i +', "name": "'+ e.attr('.label').text +'", "tokens": '+ e.prop('tokens') +' }, ';
		});
	places = places.slice(0,-2) + ']';

	var transitions = '"transitions": [';
	transArray().forEach(function(oe, oi) {
		var links_in_ids = [], links_out_ids = [];
		linkArray().forEach(function(ie, ii) {
			if(oe.id == ie.prop('source').id || oe.id == ie.prop('target').id)
				if(ie.prop('direction'))
					links_out_ids.push(ii);
				else
					links_in_ids.push(ii);
			});
		transitions += '{ "id": '+ oi +', "name": "'+ oe.attr('.label').text +'", "priority": '+ oe.prop('priority') +', "links_in_ids": '+ JSON.stringify(links_in_ids) +', "links_out_ids": '+ JSON.stringify(links_out_ids) +' }, ';
		});
	transitions = transitions.slice(0,-2) + ']';

	var links = '"links": [';
	linkArray().forEach(function(e, i) {
		links += '{ "id": '+ i +', "place_id": '+ (e.prop('direction') ? getIndex(e.prop('target').id) : getIndex(e.prop('source').id)) +', "direction": '+ e.prop('direction') +', "weight": '+ e.prop('weight') +' }, ';
		});
	links = links.slice(0,-2) + ']';

	return '"data": {'+ links +','+ places +','+ transitions +'}';
	}

//deserialize graph
function deserializeGraph(data) {
	fireTransition(transArray()[data.id], 1);
	data.links_in.concat(data.links_out).forEach(function(e) {
		e = e.place;
		placeArray()[e.id].prop('tokens', e.tokens);
		});
	}
	
//save graph to file	
function saveToFile() {
	saveAs(new Blob([JSON.stringify(petrinet.toJSON())], {type: 'text/plain;charset=utf-8'}), 'graph.txt');
	}
	
$('#save-graph').click(saveToFile);
	
//load graph from file	
function loadFromFile() {
	var file = this.files[0];
	var type = /text.*/;
	
	if(file.type.match(type)) {
		var reader = new FileReader();
		reader.onload = function(e) {
			petrinet.fromJSON(JSON.parse(reader.result));
			updatePanel();
			updateLinks();
			}
		reader.readAsText(file);
		}
	else {
		console.log('ERROR: File not supported');
		alertMsg('File not supported');
		}
	}
	
$('#load-graph').change(loadFromFile);

//web socket connection
socket = new WebSocket("ws://localhost:8888/websocket");

//response handler
socket.onmessage = function(e) {
	var data = JSON.parse(e.data);
    switch(data.type) {
        case 1:
            break;
        case 2:
		case 6:
            deserializeGraph(data.data);
        break;
		case 3:
		case 4:
			displayParams(data.data);
		break;
		case 5:
			availableTrans(data.data);
		break;
		default:
			console.log('ERROR: Unexpected response data');
        }
        console.log(e.data);
	};

//simulation
var simulation;

//display parameters type
var paramtype;

//send graph
function sendGraph() {
	socket.send('{ "type": 1, '+ serializeGraph() +' }');
	socket.send('{ "type": 5, "data" : "" }');
	}

//simulation step
function stepSimulation() {
	socket.send('{ "type": 2, "data": "" }');
	socket.send('{ "type" : 5, "data" :"" }');
	$('#fire-trans > optgroup').empty();
	transArray().forEach(function(e) {
		e.attr({ 'rect': { fill: '#000000' } });
		});
	}

//list available transitions
function availableTrans(ids) {
	ids.forEach(function(e) {
		$('#fire-trans > optgroup').append($('<option>', { value: e, text: transArray()[e].prop('name') }));
		transArray()[e].attr({ 'rect': { fill: '#33DE1D' } });
		});
	}

//fire transaction from list	
$('#fire-trans > optgroup').click(function(e) {
	socket.send('{ "type" : 6, "data" : ' + $('#fire-trans').val() + ' }');
	socket.send('{ "type" : 5, "data" :"" }');
	$(this).empty();
	transArray().forEach(function(e) {
		e.attr({ 'rect': { fill: '#000000' } });
		});
	});
	
$('#simulation-step').click(stepSimulation);

//start simulation
function startSimulation() {
	simulation = setInterval(stepSimulation, 2000);
	}

$('#simulation-start').click(startSimulation);
	
//stop simulation
function stopSimulation() {
	clearInterval(simulation);
	}
	
$('#simulation-stop').click(stopSimulation);

//get graph parameters
function getParams() {
	socket.send('{ "type" : 3 , "data" : "" }');
	}
	
$('button[data-type]').click(function() { paramtype = $(this).data('type'); getParams(); });

//vector conservative
function vectorConservative() {
	var vector = $('#weight-vector').val().trim();
	var splited = vector.split(',');
	
	if(vector && splited.length == placeArray().length) {
		var flag = true;
		var array = [];
		splited.forEach(function(e) {
			array.push(parseInt(e));
			if(!Number.isInteger(parseInt(e)))
				flag = false;
				});
		if(flag) {
			socket.send('{ "type" : 4 , "data" : "['+ array +']" }');
			}
		else {
			console.log('ERROR: Vector should contains only integers');
			alertMsg('Vector should contains only integers');
			}
		}
	else {
		console.log('ERROR: Invalid vector data');
		alertMsg('Invalid vector data');
		}
	}
	
$('#vector-conservative').click(function() { paramtype = 5; vectorConservative(); });

//display graph parameters
function displayParams(data) {
	$('#overlay').fadeIn();
	switch(paramtype) {
		case 1:
			$('#box').append($('<table>', { id: 'matrix' }));
			data[1].forEach(function(oe, oi) {
				$('#box > table').append('<tr>');
				var index = oi +1;
				oe.forEach(function(ie) {
					$('#box tr:nth-child(' + index + ')').append('<td>' + ie + '</td>');
					});
				});
		break;
		case 2:
			destroy = false;
			drawGraph(data[3]);
		break;
		case 3:
			destroy = false;
			drawGraph(data[4]);
		break;
		case 4:
			$('#box').append('Live transitions: ' + data[2]);
			$('#box').append('<br />Transitions liveness: ' + data[10]);
			$('#box').append('<br />Places K-bounded: ' + data[5]);
			$('#box').append('<br />K-bounded network: '); 
			$('#box').append(data[6] ? '<span class="glyphicon glyphicon-ok"></span>' : '<span class="glyphicon glyphicon-remove"></span>');
			$('#box').append('<br />Save network: ');
			$('#box').append(data[7] ? '<span class="glyphicon glyphicon-ok"></span>' : '<span class="glyphicon glyphicon-remove"></span>');
			$('#box').append('<br />Conservative network: ');
			$('#box').append(data[8] ? '<span class="glyphicon glyphicon-ok"></span>' : '<span class="glyphicon glyphicon-remove"></span>');
			$('#box').append('<br />Live network: ');
			$('#box').append(data[9] ? '<span class="glyphicon glyphicon-ok"></span>' : '<span class="glyphicon glyphicon-remove"></span>');
			$('#box').append('<br />Reversible network: ');
			$('#box').append(data[11] ? '<span class="glyphicon glyphicon-ok"></span>' : '<span class="glyphicon glyphicon-remove"></span>');
		break;
		case 5:
			$('#box').append('Vector conservative: ');
			$('#box').append(data ? '<span class="glyphicon glyphicon-ok"></span>' : '<span class="glyphicon glyphicon-remove"></span>');
		break;
		default:
			console.log('ERROR: Unexpected paramether type');
		}
	}

//dastroy graph
var destroy;

//draw graph
function drawGraph(data) {
	
	var graph = new joint.dia.Graph;
	
	var paper = new joint.dia.Paper({ el: $('#box'), width: windowDim.width, height: 1000, gridSize: 1, model: graph });
	
	//create graph cells
	data.forEach(function(e, i) {
		graph.addCell(new joint.shapes.fsa.State({ size: { width: 40, height: 40 }, attrs: { text : { text: e[2], 'font-size': 7 } } }));
		});

	//hilight root cell
	graph.getElements()[0].attr({ 'circle': { stroke: '#33DE1D' } });
	
	//loops
	var loops = [];
	
	//create graph links
	data.forEach(function(oe, oi) {
		if(oi > 0)
			graph.addCell(new joint.shapes.fsa.Arrow({ source: { id: graph.getElements()[oe[1]].id }, target: { id: graph.getElements()[oi].id }, labels: [{ position: .5, attrs: { text: { text: transArray()[oe[4]].prop('name') } } }] }));
		
		$.map(oe[3], function(ie, ii) {
			if(oi != ii)
				graph.addCell(new joint.shapes.fsa.Arrow({ source: { id: graph.getElements()[oi].id }, target: { id: graph.getElements()[ii].id }, labels: [{ position: .3, attrs: { text: { text: transArray()[ie].prop('name') } } }] }));
			else
				loops.push([oi, ii, ie]);
			});
		});
		
	//graph force directed layout
	var graphLayout = new joint.layout.ForceDirected({ graph: graph, width: windowDim.width, height: 1000, gravityCenter: { x: windowDim.width/2, y: 500 }, charge: 3000, linkDistance: 70 });
	
	//loop links
	var links = [];
	
	//add loop links
	loops.forEach(function(e) {
		var link = new joint.shapes.fsa.Arrow({ source: { id: graph.getElements()[e[0]].id }, target: { id: graph.getElements()[e[1]].id }, labels: [{ position: .3, attrs: { text: { text: transArray()[e[2]].prop('name') } } }] });
		graph.addCell(link);
		links.push(link);
		});

	graphLayout.start();
	
	function forceLayout() {
		if(destroy)
			return 0;
		links.forEach(function(e) {
			var cell = graph.getCell(e.prop('source'));
			e.set('vertices', [{ x: cell.x - 10, y: cell.y - 60 }, { x: cell.x + 30, y: cell.y - 60 }]);
			});
		joint.util.nextFrame(forceLayout);
		graphLayout.step();
		}
		
	forceLayout();
	}

//close overlay
$('#close').click(function() { $('#overlay').fadeOut(); destroy = true; $('#box').empty(); });

//application onload
$(function() {
	updatePanel();
	$('#overlay').hide();
	$('#build').trigger('click');
	});      