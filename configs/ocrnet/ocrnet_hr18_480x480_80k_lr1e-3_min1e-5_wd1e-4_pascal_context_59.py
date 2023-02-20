_base_ = [
    '../_base_/models/ocrnet_hr18.py',
    '../_base_/datasets/pascal_context_59.py', '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_80k.py'
]
optimizer = dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0001)
lr_config = dict(policy='poly', power=0.9, min_lr=1e-5, by_epoch=False)
norm_cfg = dict(type='SyncBN', requires_grad=True)
model = dict(
    test_cfg=dict(mode='slide', crop_size=(480, 480), stride=(320, 320)),
    pretrained='./pretrain/hrnetv2_w18-00eb2006.pth',    
    decode_head=[
    dict(
        type='FCNHead',
        in_channels=[18, 36, 72, 144],
        channels=sum([18, 36, 72, 144]),
        in_index=(0, 1, 2, 3),
        input_transform='resize_concat',
        kernel_size=1,
        num_convs=1,
        concat_input=False,
        dropout_ratio=-1,
        num_classes=59,
        norm_cfg=norm_cfg,
        align_corners=False,
        loss_decode=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=0.4)),
    dict(
        type='OCRHead',
        in_channels=[18, 36, 72, 144],
        in_index=(0, 1, 2, 3),
        input_transform='resize_concat',
        channels=512,
        ocr_channels=256,
        dropout_ratio=-1,
        num_classes=59,
        norm_cfg=norm_cfg,
        align_corners=False,
        loss_decode=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0)),
])
checkpoint_config = dict(by_epoch=False, interval=8000)
evaluation = dict(interval=4000, metric='mIoU', pre_eval=True)
