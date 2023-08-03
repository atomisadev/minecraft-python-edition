#version 330

out vec4 fragment_color;

in vec3 local_position;

void main(void) {
  vec3 green = vec3(0.0, 1.0, 0.0); // temporary, to test the 3d shader
  vec3 blue = vec3(0.0, 0.0, 1.0); // temporary, to test the 3d shader
	fragment_color = vec4(mix(green, blue, local_position.y / 2.0 + 0.5), 1.0);
}