#version 430 core

// Interpolated values from the vertex shaders
in vec2 UV;
in vec3 v;
in vec3 l;
in vec3 n;

// Ouput data
out vec4 color;

uniform mat4 M;
uniform mat4 V;
uniform vec4 lightPosition;
uniform vec3 planetColor;
uniform sampler2D sampler;

uniform vec3 diffuseAlbedo = vec3(0, 0, 1);
uniform vec3 specularAlbedo = vec3(0.1, 0.1, 0.1);

const vec4 ambient = vec4(0.1, 0.1, 0.1, 0.8);

void main(){
	vec3 n = normalize(n);
	vec3 l = normalize(l);
	vec3 v = normalize(v);
	vec3 r = reflect(-l, n);

	vec4 textureColor = texture(sampler, UV);
	vec3 diffuse = max(dot(l, n), 0.0) * textureColor.rgb;
	vec3 specular = pow(max(dot(r, v), 0.0), 12) * specularAlbedo;

	color = ambient * textureColor + vec4(diffuse + specular, 1.0);

}
