shader_type spatial;
render_mode unshaded;
// Diagnostic only: this changes shading, not geometry or collision.
uniform float tiles : hint_range(1.0, 32.0, 1.0) = 8.0;
void fragment() {
	vec2 cell = floor(UV * tiles);
	float value = mod(cell.x + cell.y, 2.0);
	ALBEDO = mix(vec3(0.12), vec3(0.92), value);
}
