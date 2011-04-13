import glob
import os.path

# ##################################################################
# Config
# ##################################################################

JSFILES = "results/*.js"
HTMLPATH = "html"

# ##################################################################
# Templates
# ##################################################################

TEMPLATE_HTML = """\
<!DOCTYPE HTML>
<html>
<head>

<title>three.js webgl - %(title)s</title>

<style type="text/css">
body {
    font-family: Monospace;
    background-color: #000;
    margin: 0px;
    overflow: hidden;
}
</style>

<script type="text/javascript" src="js/Three.js"></script>
<script type="text/javascript" src="js/Animal.js"></script>
<script type="text/javascript" src="js/Detector.js"></script>
<script type="text/javascript" src="js/RequestAnimationFrame.js"></script>

</head>

<body>

<script>

if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

var container;
var camera, scene, renderer;
var morphObject;

init();
animate();

function init() {

    container = document.createElement( 'div' );
    document.body.appendChild( container );

    camera = new THREE.Camera( 45, window.innerWidth / window.innerHeight, 1, 2000 );
    camera.position.y = 20;
    camera.position.z = 100;

    scene = new THREE.Scene();

    scene.addLight( new THREE.AmbientLight( 0xeeeeee ) );

    var light;

    light = new THREE.DirectionalLight( 0xffffff, 0.5 );
    light.position.set( 0, 1, 1 );
    //scene.addLight( light );

    renderer = new THREE.WebGLRenderer( { antialias: true, clearColor: 0x000000, clearAlpha: 1 } );
    renderer.setSize( window.innerWidth, window.innerHeight );

    container.appendChild( renderer.domElement );


    var loader = new THREE.JSONLoader();
    loader.load( { model: "../%(fname)s", callback: addAnimal } );

};

function addAnimal( geometry ) {

    morphObject = ROME.Animal( geometry, true );
    
    var mesh = morphObject.mesh;

    mesh.rotation.set( 0, -0.5, 0 );

    mesh.matrixAutoUpdate = false;
    mesh.updateMatrix();
    mesh.update();
    
    scene.addChild( mesh );

    cameraDistance = mesh.boundRadius * 3;
    cameraHeight = mesh.boundRadius * 0.1;

    camera.position.set( 0, cameraHeight, cameraDistance );
    camera.target.position.set( 0, 0, 0 );

    var nameA = morphObject.availableAnimals[ 0 ],
        nameB = morphObject.availableAnimals[ 0 ];

    morphObject.play( nameA, nameB );

};


var delta, time, oldTime = new Date().getTime();

function updateMorph( delta ) {

    if ( morphObject ) {
        
        THREE.AnimationHandler.update( delta );
        
    }

};

function animate() {

    requestAnimationFrame( animate );
    
    time = new Date().getTime();
    delta = time - oldTime;
    oldTime = time;

    updateMorph( delta );
    
    render();

};

function render() {

    renderer.render( scene, camera );

}

</script>
</body>

<html>
"""


# ##################################################################
# Utils
# ##################################################################

def write_file(name, content):
    f = open(name, "w")
    f.write(content)
    f.close()

# ##################################################################
# Main
# ##################################################################

if __name__ == "__main__":

    jsfiles = sorted(glob.glob(JSFILES))
    
    for jsname in jsfiles:

        fname = os.path.splitext(jsname)[0]
        bname = os.path.basename(fname)        

        htmlname = "%s.html" % bname
        htmlpath = os.path.join(HTMLPATH, htmlname)

        content = TEMPLATE_HTML % { 
        "fname"	: jsname.replace("\\","/"),
        "title"	: bname
        }
        
        write_file(htmlpath, content)
        