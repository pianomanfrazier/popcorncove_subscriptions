module Page.Items exposing
    ( Model
    , Msg
    , init
    , update
    , view
    )

import Html.Styled exposing (..)
import Html.Styled.Events as HSE
import Skeleton
import UI



-- Model


type alias Model =
    { num : Int }


init : Int -> ( Model, Cmd Msg )
init num =
    ( Model num, Cmd.none )



-- UPDATE


type Msg
    = NoOp
    | AddItem
    | RemoveItem


update : Msg -> Model -> ( Model, Cmd msg )
update msg model =
    case msg of
        NoOp ->
            ( model
            , Cmd.none
            )
        
        AddItem ->
            ( { model | num = model.num + 1 }
            , Cmd.none
            )

        RemoveItem ->
            ( { model | num = model.num - 1 }
            , Cmd.none
            )



-- VIEW


view : Model -> Skeleton.Details Msg
view model =
    { title = "Add Subscription Items"
    , attrs = []
    , kids =
        [ div []
            [ h1 [] [text "Subscription Items"]
            , UI.btn [ HSE.onClick RemoveItem ] [ text "Remove Item" ]
            , span [] [ text <| String.fromInt model.num ]
            , UI.btn [ HSE.onClick AddItem ] [ text "Add Item" ]
            ]
        ]
    }
