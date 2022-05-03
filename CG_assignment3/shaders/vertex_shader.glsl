#version 430 core

// Input vertex data, different for all executions of this shader.
layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec2 vertexUV;
layout(location = 2) in vec3 vertexNormal;

// Output data ; will be interpolated for each fragment.
out vec2 UV;
out vec3 v;
out vec3 l;
out vec3 n;
// Values that stay constant for the whole mesh.
uniform mat4 MVP;
uniform mat4 M;
uniform mat4 V;
uniform vec4 lightPosition;
uniform float lightBool;
uniform vec3 planetColor;

void main(){
	gl_Position =  MVP * vec4(vertexPosition, 1);
	
	vec4 p = V * M * vec4(vertexPosition, 1.0);
	
	l = lightPosition.xyz - p.xyz;
	n = lightBool * (V * M * vec4(vertexNormal, 0.0)).xyz;
	v = -p.xyz;

	//fragmentColor = vertexColor;
	UV = vertexUV;
}
