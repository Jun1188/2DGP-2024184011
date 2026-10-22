from pathlib import Path
import runpy

# 기존 이동 예제를 재사용한다. 이미지 경로는 해당 예제에서 설정한다.
source = Path(__file__).resolve().parents[2] / 'LEC06' / 'character_draws.py'
runpy.run_path(str(source), run_name='__main__')
