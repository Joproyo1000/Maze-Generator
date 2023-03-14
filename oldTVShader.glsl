#version 330 core

precision mediump float;
uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {

  vec2 center = vec2(0.5, 0.5);
  vec2 off_center = uvs - center;

  off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(2.5));

  vec2 uvs2 = center+off_center;

  if (uvs2.x > 1.0 || uvs2.x < 0.0 ||
      uvs2.y > 1.0 || uvs2.y < 0.0) {
    f_color=vec4(0.0, 0.0, 0.0, 1.0);
  }
  else {
    f_color = vec4(texture(tex, uvs2).rgb, 1.0);
    vec2 off_uvs = vec2(uvs.x * sin(uvs.y + time*0.1)*10, uvs.y);
    float fv = fract(uvs2.y/(10+sin(time)*0.1) * float(textureSize(tex,0).y));
    fv=min(1.0, 0.8+0.5*min(fv, 1.0-fv));
    f_color.rgb*=fv;
  }
}