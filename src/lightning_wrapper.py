# define the LightningModule
class LitClassifier(L.LightningModule):
    def __init__(self, classifier):
        super().__init__()
        self.classifier = classifier

    def training_step(self, batch, batch_idx):
        x, y = batch
        x = x.view(x.size(0), -1)
        pred = self.classifier(x)
        loss = nn.functional.mse_loss(pred, y)
        self.log("train_loss", loss)
        return loss
    
    def test_step(self, batch, batch_idx):
        x, y = batch
        x = x.view(x.size(0), -1)
        pred = self.classifier(x)
        test_loss = F.mse_loss(pred, y)
        self.log("test_loss", test_loss)
        
    def validation_step(self, batch, batch_idx):
        x, y = batch
        x = x.view(x.size(0), -1)
        pred = self.classifier(x)
        test_loss = F.mse_loss(pred, y)
        self.log("val_loss", test_loss)

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


# init the Classifier
classifier = LitClassifier(GenreFCN())

# train model
trainer = L.Trainer()
trainer.fit(model=classifier, train_loader, valid_loader)
