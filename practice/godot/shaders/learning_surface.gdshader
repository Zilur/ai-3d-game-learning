shader_type spatial;
render_mode cull_back;
uniform vec4 tint : source_color = vec4(0.23, 0.56, 0.42, 1.0);
uniform float wind_amount : hint_range(0.0, 0.25) = 0.0;
uniform float rim_amount : hint_range(0.0, 2.0) = 0.0;
uniform float clock = 0.0;
uniform bool stripe = false;
void vertex() {
	// A bounded visual deformation only; physics shapes are not modified.
	VERTEX.x += sin(clock * 1.8 + VERTEX.y * 2.2) * wind_amount * smoothstep(0.0, 1.8, VERTEX.y);
}
void fragment() {
	float pattern = stripe ? mix(0.7, 1.0, step(0.5, fract(UV.y * 8.0))) : 1.0;
	ALBEDO = tint.rgb * pattern;
	ROUGHNESS = 0.85;
	float rim = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 3.0);
	EMISSION = tint.rgb * rim * rim_amount;
}
