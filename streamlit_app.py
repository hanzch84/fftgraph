import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Multi-band Audio Visualizer", page_icon="🎵", layout="wide")

st.title("다중 주파수 대역 오디오 시각화")

# p5.js 스크립트
p5_script = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/addons/p5.sound.min.js"></script>
<div id="p5sketch"></div>
<script>
let mic, fft;
const bands = 5;
const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF'];

function setup() {
  let cnv = createCanvas(600, 500);
  cnv.parent('p5sketch');
  
  mic = new p5.AudioIn();
  mic.start();

  fft = new p5.FFT(0.8, 1024);
  fft.setInput(mic);
}

function draw() {
  background(0);
  
  let spectrum = fft.analyze();
  let bandSize = spectrum.length / bands;
  
  for (let i = 0; i < bands; i++) {
    let start = i * bandSize;
    let end = start + bandSize;
    let bandSpectrum = spectrum.slice(start, end);
    
    stroke(colors[i]);
    noFill();
    beginShape();
    for (let j = 0; j < bandSpectrum.length; j++) {
      let x = map(j, 0, bandSpectrum.length, 0, width);
      let y = map(bandSpectrum[j], 0, 255, height - i*height/bands, height - (i+1)*height/bands);
      vertex(x, y);
    }
    endShape();
  }
}
</script>
"""

# Streamlit 앱
st.markdown("이 앱은 p5.js를 사용하여 마이크 입력의 실시간 다중 주파수 대역 오디오 시각화를 보여줍니다.")
st.markdown("각 색상은 다른 주파수 대역을 나타냅니다.")

if st.button('Start/Stop Visualization'):
    components.html(p5_script, height=550)

st.markdown("""
### 사용 방법:
1. 'Start/Stop Visualization' 버튼을 클릭하여 시각화를 시작합니다.
2. 브라우저에서 마이크 사용 권한을 요청하면 '허용'을 클릭합니다.
3. 말을 하거나 소리를 내보세요. 화면에서 실시간으로 변화하는 시각화를 볼 수 있습니다.
4. 시각화를 중지하려면 다시 버튼을 클릭하세요.
""")

st.markdown("""
### 시각화 설명:
- 화면은 5개의 주파수 대역으로 나뉘어 있습니다.
- 각 색상은 다른 주파수 대역을 나타냅니다:
  - 빨간색: 최저 주파수
  - 초록색: 저주파
  - 파란색: 중간 주파수
  - 노란색: 고주파
  - 보라색: 최고 주파수
- 각 대역 내에서 파형의 높이는 해당 주파수의 강도를 나타냅니다.
""")