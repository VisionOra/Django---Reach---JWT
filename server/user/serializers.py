from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Profile
from user.services import get_ethereum_balance


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})
    ethereum_wallet_address = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
            "ethereum_wallet_address",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def save(self):
        print(
            "self.validated_data at serialzer+++: ",
            self.validated_data["ethereum_wallet_address"],
        )

        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        # Fetch the Ethereum balance
        address = self.validated_data["ethereum_wallet_address"]
        balance = get_ethereum_balance(address)

        # Create or update the user profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.ethereum_wallet_address = address
        profile.ethereum_balance = balance

        profile.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "about",
            "ethereum_wallet_address",
            "ethereum_balance",
        )


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(source="profile", read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "first_name", "last_name", "user_profile")
