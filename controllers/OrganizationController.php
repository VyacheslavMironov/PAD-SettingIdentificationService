<?php

namespace app\controllers;

use Yii;
use yii\filters\Cors;

class OrganizationController extends \yii\rest\ActiveController
{
    // public $modelClass = 'app\models\Organization';
    // public $enableCsrfValidation = false;

    // /**
    //  * @inheritdoc
    //  */
    // public function behaviors()
    // {
    //     $behaviors = parent::behaviors();
    //     $behaviors['corsFilter'] = [
    //         'class' => Cors::class,
    //         'cors' => [
    //             'Origin' => ['*'],
    //             'Access-Control-Allow-Origin' => ['*'],
    //             'Access-Control-Request-Methods' => ['POST', 'GET', 'PUT', 'DELETE', 'OPTIONS'],
    //             'Access-Control-Max-Age' => 3600,
    //             'Access-Control-Expose-Headers' => ['X-Pagination-Current-Page'],
    //             'Access-Control-Request-Headers' => ['*'],
    //             'Access-Control-Allow-Headers' => ['X-Requested-With', 'Content-Type', 'Accept', 'Authorization'],
    //             #'Access-Control-Expose-Headers' => ['*'],
    //         ],
    //     ];
    //     return $behaviors;
    // }

    // public function actionAdd() {
    //     $this->behaviors();
    //     $request = Yii::$app->request;
    //     return $this->asJson(array(['a' => 123]));
    // }

}
