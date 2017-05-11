from opts import args
from models import create_model
from datasets import create_loader
# from train import Trainer
# from log import Logger

def main():
    # Create Model, Criterion and State
    model, criterion, state = create_model(args)
    print "=> Model and criterion are ready"
    # Create Dataloader
    train_loader = create_loader(args, 'train')
    val_loader = create_loader(args, 'val')
    print "=> Dataloaders are ready"
    # Create logger
    logger = Logger(args, state)
    print "=> Logger is ready"
    # Create trainer 
    trainer = Trainer(args, model, criterion, logger)
    print "=> Trainer is ready"

    if args.test_only:
        test_summary = trainer.test(0, val_loader)
        print "Top1 Error: %6.3f  Top5 Error: %6.3f" % (test_summary[0], test_summary[1])
        # If unnecessary, comment the following line
        logger.record(test=test_summary)

    start_epoch = logger.start_epoch
    for epoch in xrange(start_epoch, args.n_epochs + 1):
        train_summary = trainer.train(epoch, train_loader)
        test_summary = trainer.test(epoch, val_loader)

        logger.record(train=train_summary, test=test_summary, epoch=epoch, model=model) 

    logger.final_print()

if __name__ == '__main__':
    main()
