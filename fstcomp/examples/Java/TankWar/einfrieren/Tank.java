
public class Tank {

	protected long einfrierenTimer;
	protected boolean einfrieren = false;
	
	protected void toolKontroller(){
		original();
		if (tankManager.status == GameManager.PAUSE || tankManager.status == GameManager.EXIT) {
			if (einfrieren) {
				einfrierenTimer += elapsedTime;
			}
		}
		if (einfrieren && System.currentTimeMillis() - einfrierenTimer > 8000) {
			for (int i = 0; i < tankManager.tankMenge.size(); i++) {
				if (tankManager.tankMenge.elementAt(i) != this) {
					((Tank) tankManager.tankMenge.elementAt(i)).aktive = true;
				}
			}
			einfrieren = false;
		}
	}

	protected void toolBehandeln(int toolType) {
		original(toolType);
		switch (toolType) {
		case 371:// 100,149,237
			this.einfrierenTimer = System.currentTimeMillis();
			this.einfrieren = true;
			for (int i = 0; i < tankManager.tankMenge.size(); i++) {
				if (tankManager.tankMenge.elementAt(i) != tankManager.tank1
						&& tankManager.tankMenge.elementAt(i) != tankManager.tank2) {
					((Tank) tankManager.tankMenge.elementAt(i)).aktive = false;
				}
			}
			break;
		}
	}

}