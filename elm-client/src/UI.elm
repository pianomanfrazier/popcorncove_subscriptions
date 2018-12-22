module UI exposing (btn)

import Css exposing (backgroundColor, em, hex, inlineBlock, margin, padding2, px)
import Html.Styled exposing (Attribute, Html, button, styled)
import Html.Styled.Attributes as HSA exposing (checked, css, value)
import Html.Styled.Events as HSE exposing (onCheck, onClick, onInput)


{-| A reusable button which has some styles pre-applied to it.
-}
btn : List (Attribute msg) -> List (Html msg) -> Html msg
btn =
    styled button
        [ margin (em 1)
        , padding2 (px 12) (px 20)
        , Css.display inlineBlock
        , Css.border3 (px 1) Css.solid (hex "BBB")
        , Css.borderRadius (px 4)
        , Css.cursor Css.pointer
        , backgroundColor (hex "EEE")
        , Css.hover
            [ backgroundColor (Css.rgba 155 155 155 0.3)
            ]
        ]
