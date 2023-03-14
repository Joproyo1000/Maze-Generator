#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Sample the texture
    vec2 sample_pos = vec2(uvs.x, uvs.y);
    vec4 color = texture(tex, sample_pos);

    // Determine the brightness of the pixel
    float brightness = (color.r + color.g + color.b) / 5.0;

    // Apply a threshold to the brightness
    float threshold = 0.2;
    float alpha = smoothstep(threshold - 0.05, threshold + 0.05, brightness);

    // Blur the bright areas using a box filter
    float blurSize = 0.004;
    vec4 blur = vec4(0.0);
    for (int i = -4; i <= 4; i++) {
        blur += texture(tex, uvs + vec2(i, 0.0) * blurSize) * alpha / 9.0;
        blur += texture(tex, uvs + vec2(0.0, i) * blurSize) * alpha / 9.0;
    }

    // Combine the blurred image with the original image
    float mixAmount = 0.6;

    f_color = mix(color, blur, mixAmount);
}