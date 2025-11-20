var canvas = document.querySelector('canvas');

canvas.width = 1000;
canvas.height = 1000;
// canvas.style.position = 'relative'
// canvas.style.top = '0%'
// canvas.style.left = '20%'

var c = canvas.getContext('2d');
//var config_file_name = window.prompt('Enter the .json config file name: ');
var config_file_name = "";

var draw_planets = true;
function drawPlanets() {
    draw_planets = !draw_planets;
}
var draw_trails = true;
function drawTrails() {
    draw_trails = !draw_trails;
}
var draw_connect = true;
function drawConnect() {
    draw_connect = !draw_connect;
}
var edit_mode = false;
function editMode() {
    edit_mode = !edit_mode;
}
var bR = 0;
function bgr(red_val) {
    if (edit_mode) {
        bR = red_val;
    }
}
var bG = 0;
function bgg(green_val) {
    if (edit_mode) {
        bG = green_val;
    }
}
var bB = 0;
function bgb(blue_val) {
    if (edit_mode) {
        bB = blue_val;
    }
}
var cR = 0;
function cor(red_val) {
    if (edit_mode) {
        cR = red_val;
    }
}
var cG = 0;
function cog(green_val) {
    if (edit_mode) {
        cG = green_val;
    }
}
var cB = 0;
function cob(blue_val) {
    if (edit_mode) {
        cB = blue_val;
    }
}
var cO = 1;
function coo(blue_val) {
    if (edit_mode) {
        cO = blue_val;
    }
}
var trail_width = 1;
function trail_stroke(ts) {
    if (edit_mode) {
        trail_width = ts;
    }
}
var TRAIL_LENGTH = 1;
function t_length(tl) {
    if (edit_mode) {
        TRAIL_LENGTH = tl;
    }
}
var CONNECT_DENSITY = 1;
function c_density(cd) {
    if (edit_mode) {
        CONNECT_DENSITY = cd;
    }
}
var connect_width = 1;
function con_stroke(cs) {
    if (edit_mode) {
        connect_width = cs;
    }
}
var select_planet = 0;
function selected_planet(sp) {
    if (edit_mode) {
        select_planet = sp;
    }
}
var curr_radius = 0;
function selected_radius(sr) {
    if (edit_mode) {
        curr_radius = sr;
    }
}
var pR = 0;
function pr(red_val) {
    if (edit_mode) {
        pR = red_val;
    }
}
var pG = 0;
function pg(green_val) {
    if (edit_mode) {
        pG = green_val;
    }
}
var pB = 0;
function pb(blue_val) {
    if (edit_mode) {
        pB = blue_val;
    }
}
var pO = 1;
function po(blue_val) {
    if (edit_mode) {
        pO = blue_val;
    }
}

function drawCircle(ctx, x, y, radius, fill) {
    ctx.beginPath()
    ctx.arc(x, y, radius, 0, 2 * Math.PI, false)
    ctx.fillStyle = fill
    ctx.fill()
}

class Obj {
    constructor (radius, init_position, color, name, connect) {
        this.radius = radius;
        this.position = init_position;
        this.color = color;
        this.name = name;
        this.color = color;
        this.connect = connect;
        this.points = [init_position]
    }

    draw(cv, tl) {
        if (draw_planets) {
            drawCircle(cv, this.position[0], this.position[1], this.radius, this.color)
        }

        this.points.push(this.position);
        while (this.points.length >= tl) {
            this.points.shift()
        }
        if (draw_trails) {
            cv.beginPath();
            cv.moveTo(this.points[0][0], this.points[0][1]);
            for (var p = 1; p < this.points.length; p++) {
                cv.lineTo(this.points[p][0], this.points[p][1]);
            }
            cv.strokeStyle = this.color
            cv.lineWidth = trail_width;
            cv.stroke();
        }
        
    }

    connect_planets(cv, bodies, cd, cc, cw) {
        for (var u = 0; u < bodies.length; u++) {
            var connect_points = [];
            if (this.connect && bodies[u].connect) {
                for (var v = 0; v < this.points.length - 1; v = v + cd) {
                    connect_points.push([this.points[v], bodies[u].points[v]]);
                }
            }
            //console.log(connect_points);
            if (this.connect) {
                cv.beginPath()
                for (var v = 0; v < connect_points.length; v++) {
                    cv.moveTo(connect_points[v][0][0], connect_points[v][0][1]);
                    cv.lineTo(connect_points[v][1][0], connect_points[v][1][1]);
                }
                cv.strokeStyle = cc;
                cv.lineWidth = cw;
                cv.stroke();
            }
        }
    }
}

function ljson(config_name) {
    config_file_name = config_name;
    var planets = [];
    var bg_color = 'rgba(0, 0, 0, 0)';
    var con_color = 'rgba(0, 0, 0, 0)';

    $.getJSON(`/scripts/${config_file_name}.json`, function(data){
        for (const [key, value] of Object.entries(data)) {
            if (key == 'main'){
                TRAIL_LENGTH = parseInt(value[0]['trail_length']);
                CONNECT_DENSITY = parseInt(value[0]['connect_density']);
                raw_bg = value[0]["bg_color"];
                bR = raw_bg.split(',')[0];
                bG = raw_bg.split(',')[1];
                bB = raw_bg.split(',')[2];
                // bg_color = `rgba(${raw_bg.split(',')[0]}, ${raw_bg.split(',')[1]}, ${raw_bg.split(',')[2]}, 1.0)`;
                raw_con = value[0]["con_color"];
                cR = raw_con.split(',')[0];
                cG = raw_con.split(',')[1];
                cB = raw_con.split(',')[2];
                // con_color = `rgba(${raw_con.split(',')[0]}, ${raw_con.split(',')[1]}, ${raw_con.split(',')[2]}, 1.0)`;
            }
            else {
                raw_pos = value[0]["init_position"];
                ipos = [parseFloat(raw_pos.split(',')[0]), parseFloat(raw_pos.split(',')[1])];
                raw_col = value[0]["color"];
                col = `rgba(${raw_col.split(',')[0]}, ${raw_col.split(',')[1]}, ${raw_col.split(',')[2]}, 1.0)`;
                planets.push(new Obj(parseFloat(value[0]["radius"]), ipos, col, key, (value[0]["connect"] == "True")));
            }
        }
        document.getElementById("t_length").value = TRAIL_LENGTH;
        document.getElementById("con_density").value = CONNECT_DENSITY;
        document.getElementById("planet_select").max = planets.length - 1;
        document.getElementById("bg_red").value = bR;
        document.getElementById("bg_green").value = bG;
        document.getElementById("bg_blue").value = bB;
        document.getElementById("con_red").value = cR;
        document.getElementById("con_green").value = cG;
        document.getElementById("con_blue").value = cB;
        document.getElementById("con_opacity").value = cO;
        curr_radius = planets[select_planet].radius;
        document.getElementById("selected radius").value = curr_radius;
        var curr_color = planets[select_planet].color;
        document.getElementById("p_red").value = curr_color.slice(5, curr_color.length).split(',')[0];
        document.getElementById("p_green").value = curr_color.slice(5, curr_color.length).split(',')[1].slice(1);        
        document.getElementById("p_blue").value = curr_color.slice(5, curr_color.length).split(',')[2].slice(1);
        document.getElementById("p_opacity").value = curr_color.slice(5, curr_color.length - 1).split(',')[3].slice(1);

        var lines = [];
        $.get(`/scripts/${config_file_name}_pos_log.txt`, function(data){
            lines = data.split(/\r?\n/);
            var positions = [];
            for (var k = 0; k < lines.length; k++) {
                let line = lines[k].split(',');
                positions.push([line[0], parseFloat(line[1]), parseFloat(line[2])])
            }
            var init_positions = positions.slice();
            var count = 0;
            
            function animate() {
                requestAnimationFrame(animate);
                c.fillStyle = bg_color;
                c.fillRect(0, 0, 1000, 1000);
                
                planets[select_planet].radius = curr_radius;
                planets[select_planet].color = `rgba(${pR},${pG},${pB},${pO})`
                bg_color = `rgba(${bR},${bG},${bB}, 1.0)`;
                con_color = `rgba(${cR},${cG},${cB},${cO})`;
    
                var four = [];
                for (var j = 0; j < planets.length; j++) {
                    if (count >= init_positions.length) {
                        planets[j].points = [positions[j][1], positions[j][2]];
                        positions = init_positions.slice();
                    }
                    planets[j].position = [positions[j][1], positions[j][2]]
                    planets[j].draw(c, TRAIL_LENGTH);
                    if (draw_connect) {
                        planets[j].connect_planets(c, planets, CONNECT_DENSITY, con_color, connect_width);
                    }
                    four.push(positions[j]);
                    count = count + 1;
                }
    
                if (count > positions.length) {
                    count = 0;
                }
    
                positions = positions.slice(planets.length);
                for (var f = 0; f < four.length; f++) {
                    positions.push(four[f]);
                }
            }
    
            animate();
        }, 'text');
    });
}
