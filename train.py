import sys
sys.path.append('core')
import torch
from brain import AwarenessDecayNetwork

def train(epochs=100):
    model = AwarenessDecayNetwork()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    
    for i in range(epochs):
        x = torch.randn(2)
        target = torch.tensor([1.0])
        
        result, confidence, vetoed = model(x)
        
        if vetoed:
            loss = confidence
            # Note: If you want your custom weight dissolution here,
            # you need your 'with torch.no_grad():' block from earlier!
        else:
            loss = torch.nn.MSELoss()(result, target)
            
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    # FIX: These two lines must be indented 4 spaces to stay inside train()
    torch.save(model.state_dict(), "brain_weights.pth")    
    print("Training complete ✓")

if __name__ == "__main__":
    train()
    