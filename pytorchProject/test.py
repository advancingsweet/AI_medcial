import torch.nn as nn
from myconfig.Config import *
from trans1utils.DataGenerater import *
from transformer.Transformer import Transformer

vocab,vocab_size = vocab_config()
hla_max_len,pep_max_len,tcr_max_len,hla_pep_concat_len,pep_tcr_concat_len = data_config()
d_model, d_ff, d_k, d_v, _, n_heads, epochs, batch_size, threshold, dropout_rate, max_len, device \
    = model_config()
seed = run_config()

train_pep_tcr_loader,test_pep_tcr_loader \
    = pep_tcr_data_loader('pep_tcr_dataset',vocab,pep_max_len,tcr_max_len,batch_size,0.9)


model = Transformer(vocab_size, n_enc_layers=9, n_enc_heads=5, n_dec_layers=9,
                                n_dec_heads=5, hla_pep_concat_len=hla_pep_concat_len,
                                pep_tcr_concat_len=pep_tcr_concat_len,device=device).to(device)

model.load_state_dict(torch.load('../pytorchProject/model/model_pt_layer9_head5_fold4.pth'))

criterion = nn.CrossEntropyLoss()
model.eval_per_epoch(train_pep_tcr_loader,None,None,criterion,2,0.5,True)
model.eval_per_epoch(test_pep_tcr_loader,None,None,criterion,2,0.5,True)